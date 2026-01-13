from flask import Blueprint, jsonify
import os
from core.engine import Engine

pipelines_bp = Blueprint('pipelines', __name__)
engine = Engine()

@pipelines_bp.route('/pipelines')
def list_pipelines():
    workflows_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'workflows')
    pipelines = []
    for file in os.listdir(workflows_dir):
        if file.endswith('.yaml'):
            workflow = engine.load_workflow(os.path.join(workflows_dir, file))
            pipelines.append({
                'name': workflow['name'],
                'file': file,
                'steps': len(workflow.get('steps', []))
            })
    return jsonify(pipelines)