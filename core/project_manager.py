import os
import shutil
from datetime import datetime
import yaml
from core.config import Config
from core.logger import logger

class ProjectManager:
    def __init__(self, base_dir=None):
        self.config = Config()
        self.base_dir = base_dir or os.path.expanduser("~/biobuntu/projects")
        os.makedirs(self.base_dir, exist_ok=True)
    
    def create_project(self, name, description=""):
        """Create a new project with standard directory structure."""
        project_dir = os.path.join(self.base_dir, name)
        if os.path.exists(project_dir):
            raise ValueError(f"Project {name} already exists")
        
        # Create directory structure
        dirs = [
            'raw_data',
            'qc',
            'processed',
            'results',
            'reports',
            'logs',
            'config'
        ]
        
        for dir_name in dirs:
            os.makedirs(os.path.join(project_dir, dir_name), exist_ok=True)
        
        # Create project config
        project_config = {
            'name': name,
            'description': description,
            'created': datetime.now().isoformat(),
            'status': 'created'
        }
        
        import yaml
        with open(os.path.join(project_dir, 'config', 'project.yaml'), 'w') as f:
            yaml.dump(project_config, f)
        
        logger.info(f"Created project: {name}")
        return project_dir
    
    def list_projects(self):
        """List all projects."""
        projects = []
        if os.path.exists(self.base_dir):
            for item in os.listdir(self.base_dir):
                project_dir = os.path.join(self.base_dir, item)
                if os.path.isdir(project_dir):
                    config_file = os.path.join(project_dir, 'config', 'project.yaml')
                    if os.path.exists(config_file):
                        with open(config_file, 'r') as f:
                            config = yaml.safe_load(f)
                        projects.append(config)
        return projects
    
    def get_project(self, name):
        """Get project information."""
        project_dir = os.path.join(self.base_dir, name)
        config_file = os.path.join(project_dir, 'config', 'project.yaml')
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return yaml.safe_load(f)
        return None
    
    def delete_project(self, name):
        """Delete a project."""
        project_dir = os.path.join(self.base_dir, name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
            logger.info(f"Deleted project: {name}")
        else:
            raise ValueError(f"Project {name} not found")