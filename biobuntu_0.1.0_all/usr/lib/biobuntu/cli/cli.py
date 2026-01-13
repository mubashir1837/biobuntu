import click
import os
from core.engine import Engine
from core.logger import logger

@click.group()
def main():
    """BioBuntu CLI"""
    pass

@main.command()
@click.argument('workflow', type=click.Path(exists=True))
@click.option('--input', 'input_files', multiple=True, help='Input files')
@click.option('--output', 'output_dir', type=click.Path(), help='Output directory')
def run(workflow, input_files, output_dir):
    """Run a workflow pipeline."""
    try:
        engine = Engine()
        engine.run_pipeline(workflow, input_files=list(input_files), output_dir=output_dir)
        click.echo("Pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

@main.command()
def list():
    """List available workflows."""
    workflows_dir = os.path.join(os.path.dirname(__file__), '..', 'workflows')
    for file in os.listdir(workflows_dir):
        if file.endswith('.yaml'):
            click.echo(file[:-5])  # Remove .yaml

@main.command()
@click.argument('name')
@click.option('--description', default='', help='Project description')
def create_project(name, description):
    """Create a new project."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    try:
        project_dir = pm.create_project(name, description)
        click.echo(f"Project '{name}' created at {project_dir}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@main.command()
def list_projects():
    """List all projects."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    projects = pm.list_projects()
    if projects:
        for project in projects:
            click.echo(f"{project['name']}: {project['description']} ({project['status']})")
    else:
        click.echo("No projects found")

@main.command()
@click.argument('name')
def delete_project(name):
    """Delete a project."""
    from core.project_manager import ProjectManager
    pm = ProjectManager()
    try:
        pm.delete_project(name)
        click.echo(f"Project '{name}' deleted")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

@main.command()
@click.argument('workflow')
@click.option('--project', help='Project name')
@click.option('--input', 'input_files', multiple=True, help='Input files')
@click.option('--output', 'output_dir', type=click.Path(), help='Output directory')
@click.option('--parallel/--no-parallel', default=True, help='Run steps in parallel')
def run(workflow, project, input_files, output_dir, parallel):
    """Run a workflow pipeline."""
    try:
        engine = Engine()
        engine.run_pipeline(workflow, input_files=list(input_files), output_dir=output_dir, project=project, parallel=parallel)
        click.echo("Pipeline completed successfully")
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()

@main.command()
@click.argument('workflow')
def validate(workflow):
    """Validate a workflow file."""
    try:
        engine = Engine()
        engine.validate_workflow(workflow)
        click.echo("Workflow is valid")
    except Exception as e:
        click.echo(f"Validation failed: {e}", err=True)

@main.command()
def web():
    """Start the web dashboard."""
    from web.api import app
    click.echo("Starting web dashboard on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)

@main.command()
def gui():
    """Start the GUI application."""
    try:
        from gui.main import main
        main()
    except ImportError:
        click.echo("GUI not available (tkinter not installed)", err=True)

if __name__ == "__main__":
    main()