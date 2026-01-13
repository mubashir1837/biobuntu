from flask import Flask, request, jsonify, render_template, send_file
import os
import uuid
import threading
from core.engine import Engine
from core.project_manager import ProjectManager
from .routes.pipelines import pipelines_bp
from .routes.projects import projects_bp
from .routes.status import status_bp

# Get the directory of this file (web/api.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__,
            template_folder=os.path.join(current_dir, 'templates'),
            static_folder=os.path.join(current_dir, 'static'))

engine = Engine()
project_manager = ProjectManager()

# Store for remote jobs
remote_jobs = {}

app.register_blueprint(pipelines_bp, url_prefix='/api')
app.register_blueprint(projects_bp, url_prefix='/api')
app.register_blueprint(status_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/workflows')
def get_workflows():
    workflows_dir = os.path.join(os.path.dirname(__file__), '..', 'workflows')
    workflows = []
    for file in os.listdir(workflows_dir):
        if file.endswith('.yaml'):
            workflow = engine.load_workflow(os.path.join(workflows_dir, file))
            workflows.append({
                'name': workflow['name'],
                'file': file,
                'description': workflow.get('description', '')
            })
    return jsonify(workflows)

@app.route('/api/remote/run', methods=['POST'])
def remote_run():
    """Remote pipeline execution endpoint."""
    data = request.json
    workflow = data.get('workflow')
    project = data.get('project')
    input_files = data.get('input_files', [])
    callback_url = data.get('callback_url')  # For webhook notifications
    
    if not workflow or not project:
        return jsonify({'error': 'Workflow and project are required'}), 400
    
    job_id = str(uuid.uuid4())
    remote_jobs[job_id] = {
        'status': 'queued',
        'workflow': workflow,
        'project': project,
        'input_files': input_files,
        'callback_url': callback_url
    }
    
    # Start execution in background
    thread = threading.Thread(target=execute_remote_job, args=(job_id,))
    thread.start()
    
    return jsonify({
        'job_id': job_id,
        'status': 'queued',
        'message': 'Job submitted for remote execution'
    })

@app.route('/api/remote/status/<job_id>')
def remote_status(job_id):
    """Check status of remote job."""
    if job_id not in remote_jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(remote_jobs[job_id])

@app.route('/api/remote/jobs')
def list_remote_jobs():
    """List all remote jobs."""
    return jsonify(list(remote_jobs.values()))

@app.route('/api/download/<project>/<path>')
def download_file(project, path):
    """Download files from project directory."""
    project_dir = os.path.join(project_manager.base_dir, project)
    file_path = os.path.join(project_dir, path)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

def execute_remote_job(job_id):
    """Execute a remote job."""
    job = remote_jobs[job_id]
    job['status'] = 'running'
    
    try:
        workflow_file = f"workflows/{job['workflow']}.yaml"
        engine.run_pipeline(workflow_file, input_files=job['input_files'], project=job['project'])
        job['status'] = 'completed'
        job['result'] = 'success'
    except Exception as e:
        job['status'] = 'failed'
        job['error'] = str(e)
    
    # Send callback if provided
    if job.get('callback_url'):
        import requests
        try:
            requests.post(job['callback_url'], json=job)
        except:
            pass  # Ignore callback failures

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)