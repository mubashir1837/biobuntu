# Web Dashboard

The BioBuntu web dashboard provides browser-based access to all platform features with remote execution capabilities.

## Features

- **Project Management**: Create, view, and delete analysis projects
- **Pipeline Execution**: Run workflows locally or remotely
- **Job Monitoring**: Track remote job status and progress
- **File Downloads**: Access results and intermediate files
- **Real-time Updates**: Live status updates for running jobs
- **Remote Lab Support**: API endpoints for integration with external systems

## Getting Started

Start the web server:
```bash
biobuntu web
```

Access the dashboard at: http://localhost:5000

## Interface Overview

### Projects Section
- **Create Project**: Add new analysis projects with descriptions
- **Project List**: View all projects with status and actions
- **Delete Project**: Remove projects and associated data

### Workflows Section
- **Available Pipelines**: Browse supported analysis workflows
- **Workflow Details**: View pipeline descriptions and steps

### Pipeline Execution
- **Local Execution**: Run pipelines directly on the server
- **Remote Execution**: Submit jobs to remote execution queues
- **Callback URLs**: Configure webhooks for job completion notifications

### Remote Jobs
- **Job Queue**: View all submitted remote jobs
- **Status Tracking**: Monitor job progress and completion
- **Error Reporting**: View job failures and error messages

## API Endpoints

### Projects
```
GET  /api/projects           # List all projects
POST /api/projects           # Create new project
GET  /api/projects/<name>    # Get project details
DELETE /api/projects/<name>  # Delete project
```

### Workflows
```
GET /api/workflows           # List available workflows
```

### Pipelines
```
GET /api/pipelines            # List pipelines with details
POST /api/run                # Execute pipeline locally
```

### Remote Execution
```
POST /api/remote/run                 # Submit remote job
GET  /api/remote/status/<job_id>     # Check job status
GET  /api/remote/jobs                # List all remote jobs
```

### Downloads
```
GET /api/download/<project>/<path>   # Download project files
```

### System
```
GET /api/status               # System status and version
```

## Remote Lab Integration

### Job Submission
Submit jobs programmatically:
```python
import requests

response = requests.post('http://localhost:5000/api/remote/run', json={
    'workflow': 'rnaseq.yaml',
    'project': 'myproject',
    'input_files': ['sample.fastq'],
    'callback_url': 'https://myapp.com/webhook'
})

job_id = response.json()['job_id']
```

### Status Monitoring
Check job status:
```python
status = requests.get(f'http://localhost:5000/api/remote/status/{job_id}')
print(status.json())
```

### Webhook Callbacks
Receive notifications when jobs complete:
```python
# Your webhook endpoint
@app.route('/webhook', methods=['POST'])
def job_callback():
    data = request.json
    print(f"Job {data['job_id']} completed with status: {data['status']}")
    return 'OK'
```

## Configuration

### Server Settings
- **Host**: Default 0.0.0.0 (accessible from network)
- **Port**: Default 5000
- **Debug Mode**: Enable for development

### Security
- Configure firewall rules for remote access
- Use HTTPS in production environments
- Implement authentication for multi-user setups

## Troubleshooting

### Common Issues

**Server won't start**: Check if port 5000 is available
**Jobs stuck in queue**: Verify worker processes are running
**File downloads fail**: Check project permissions and file paths
**API timeouts**: Increase timeout values for long-running jobs

### Logs

Web server logs are displayed in the terminal. For detailed application logs, check:
- Project-specific logs in `~/biobuntu/projects/project_name/logs/`
- System logs for server errors