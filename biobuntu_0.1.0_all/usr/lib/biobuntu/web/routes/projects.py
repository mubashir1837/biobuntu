from flask import Blueprint, jsonify, request
import os
from core.project_manager import ProjectManager

projects_bp = Blueprint('projects', __name__)
project_manager = ProjectManager()

@projects_bp.route('/projects', methods=['GET'])
def list_projects():
    """List all projects"""
    try:
        projects = project_manager.list_projects()
        return jsonify([{
            'name': p['name'],
            'description': p.get('description', ''),
            'created': p.get('created', ''),
            'status': p.get('status', 'unknown')
        } for p in projects])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Project name is required'}), 400

        name = data['name']
        description = data.get('description', '')

        project_dir = project_manager.create_project(name, description)
        return jsonify({
            'message': f'Project "{name}" created successfully',
            'project_dir': project_dir
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<name>', methods=['GET'])
def get_project(name):
    """Get project details"""
    try:
        project = project_manager.get_project(name)
        if project:
            return jsonify({
                'name': project['name'],
                'description': project.get('description', ''),
                'created': project.get('created', ''),
                'status': project.get('status', 'unknown'),
                'path': os.path.join(project_manager.base_dir, name)
            })
        return jsonify({'error': 'Project not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@projects_bp.route('/projects/<name>', methods=['DELETE'])
def delete_project(name):
    """Delete a project"""
    try:
        project_manager.delete_project(name)
        return jsonify({'message': f'Project "{name}" deleted successfully'})
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500