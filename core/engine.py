import yaml
import os
import importlib
import concurrent.futures
from .config import Config
from .logger import logger
from .project_manager import ProjectManager

class Engine:
    def __init__(self, config=None, project_manager=None):
        self.config = config or Config()
        self.project_manager = project_manager or ProjectManager()
        self.tools = {}
        self._load_tools()
    
    def _load_tools(self):
        """Load tool modules."""
        tools_dir = os.path.join(os.path.dirname(__file__), '..', 'tools')
        for file in os.listdir(tools_dir):
            if file.endswith('.py') and file != '__init__.py':
                module_name = file[:-3]
                module = importlib.import_module(f'tools.{module_name}')
                self.tools[module_name] = module
    
    def load_workflow(self, workflow_file):
        """Load workflow from YAML file."""
        with open(workflow_file, 'r') as f:
            workflow = yaml.safe_load(f)
        return workflow
    
    def run_pipeline(self, workflow_file, input_files=None, output_dir=None, project=None, parallel=True):
        """
        Run a pipeline with advanced features.
        """
        workflow = self.load_workflow(workflow_file)
        logger.info(f"Running pipeline: {workflow['name']}")
        
        if project:
            project_info = self.project_manager.get_project(project)
            if not project_info:
                raise ValueError(f"Project {project} not found")
            base_dir = os.path.join(self.project_manager.base_dir, project)
            output_dir = output_dir or base_dir
        else:
            output_dir = output_dir or os.getcwd()
        
        # Build dependency graph
        steps = workflow.get('steps', [])
        completed_steps = set()
        
        def can_run_step(step):
            deps = step.get('depends_on', [])
            return all(dep in completed_steps for dep in deps)
        
        # Execute steps with dependencies
        while len(completed_steps) < len(steps):
            runnable_steps = [step for step in steps if can_run_step(step) and step['name'] not in completed_steps]
            
            if not runnable_steps:
                raise RuntimeError("Circular dependency or missing dependencies detected")
            
            if parallel and len(runnable_steps) > 1:
                # Run in parallel
                with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.get('threads', 4)) as executor:
                    futures = []
                    for step in runnable_steps:
                        future = executor.submit(self._execute_step, step, input_files, output_dir)
                        futures.append((future, step))
                    
                    for future, step in futures:
                        try:
                            future.result()
                            completed_steps.add(step['name'])
                        except Exception as e:
                            logger.error(f"Step {step['name']} failed: {e}")
                            raise
            else:
                # Run sequentially
                for step in runnable_steps:
                    try:
                        self._execute_step(step, input_files, output_dir)
                        completed_steps.add(step['name'])
                    except Exception as e:
                        logger.error(f"Step {step['name']} failed: {e}")
                        raise
        
        logger.info("Pipeline completed")
    
    def _execute_step(self, step, input_files, output_dir):
        """Execute a single step."""
        logger.info(f"Running step: {step['name']}")
        tool_name = step['tool']
        if tool_name not in self.tools:
            raise ValueError(f"Tool {tool_name} not found")
        
        tool_module = self.tools[tool_name]
        
        # Prepare arguments
        args = step.get('args', {})
        if 'input' in step:
            args['input_file'] = os.path.join(output_dir, step['input'])
        if 'output' in step:
            args['output_file'] = os.path.join(output_dir, step['output'])
        
        # Call the tool function
        func_name = f'run_{tool_name}'
        if hasattr(tool_module, func_name):
            func = getattr(tool_module, func_name)
            func(**args)
        else:
            raise ValueError(f"Function {func_name} not found in {tool_name}")
    
    def validate_workflow(self, workflow_file):
        """Validate workflow structure."""
        workflow = self.load_workflow(workflow_file)
        required_keys = ['name', 'steps']
        for key in required_keys:
            if key not in workflow:
                raise ValueError(f"Missing required key: {key}")
        
        for step in workflow['steps']:
            if 'name' not in step or 'tool' not in step:
                raise ValueError("Each step must have 'name' and 'tool'")
        
        return True