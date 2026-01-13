import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from core.engine import Engine
from core.project_manager import ProjectManager
from ..widgets.file_drop import FileDrop
from ..widgets.progress_bar import ProgressBar

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("BioBuntu Studio")
        self.root.geometry("1000x700")
        
        self.engine = Engine()
        self.project_manager = ProjectManager()
        self.current_project = None
        
        # Create menu
        self.create_menu()
        
        # Create main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Project selection
        project_frame = ttk.LabelFrame(main_frame, text="Project")
        project_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(project_frame, text="Current Project:").grid(row=0, column=0, sticky=tk.W)
        self.project_var = tk.StringVar()
        self.project_combo = ttk.Combobox(project_frame, textvariable=self.project_var, state="readonly")
        self.project_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.project_combo.bind("<<ComboboxSelected>>", self.on_project_selected)
        
        ttk.Button(project_frame, text="New Project", command=self.create_project).grid(row=0, column=2, padx=(10, 0))
        ttk.Button(project_frame, text="Refresh", command=self.load_projects).grid(row=0, column=3, padx=(10, 0))
        
        project_frame.columnconfigure(1, weight=1)
        
        # Workflow selection
        workflow_frame = ttk.LabelFrame(main_frame, text="Workflow")
        workflow_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(workflow_frame, text="Select Workflow:").grid(row=0, column=0, sticky=tk.W)
        self.workflow_var = tk.StringVar()
        self.workflow_combo = ttk.Combobox(workflow_frame, textvariable=self.workflow_var)
        self.workflow_combo['values'] = self.get_workflows()
        self.workflow_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        workflow_frame.columnconfigure(1, weight=1)
        
        # File drop area
        file_frame = ttk.LabelFrame(main_frame, text="Input Files")
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        self.file_drop = FileDrop(file_frame, self.on_files_selected)
        self.file_drop.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        progress_frame = ttk.LabelFrame(main_frame, text="Progress")
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        self.progress_bar = ProgressBar(progress_frame)
        self.progress_bar.pack(fill=tk.X, expand=True)
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        self.run_button = ttk.Button(button_frame, text="Run Pipeline", command=self.run_pipeline)
        self.run_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.validate_button = ttk.Button(button_frame, text="Validate Workflow", command=self.validate_workflow)
        self.validate_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Load initial data
        self.load_projects()
        
        # Configure grid
        main_frame.columnconfigure(0, weight=1)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.create_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Settings", command=self.open_settings)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def load_projects(self):
        projects = self.project_manager.list_projects()
        project_names = [p['name'] for p in projects]
        self.project_combo['values'] = project_names
        if project_names:
            self.project_combo.set(project_names[0])
            self.on_project_selected()
    
    def on_project_selected(self, event=None):
        project_name = self.project_var.get()
        if project_name:
            self.current_project = project_name
            # Could load project-specific settings here
    
    def create_project(self):
        dialog = ProjectDialog(self.root, self.project_manager)
        self.root.wait_window(dialog.dialog)
        self.load_projects()
    
    def open_project(self):
        # For now, just refresh
        self.load_projects()
    
    def open_settings(self):
        from .settings_window import SettingsWindow
        SettingsWindow(self.root)
    
    def get_workflows(self):
        workflows_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'workflows')
        workflows = []
        for file in os.listdir(workflows_dir):
            if file.endswith('.yaml'):
                workflows.append(file[:-5])
        return workflows
    
    def on_files_selected(self, files):
        pass  # Could update UI
    
    def run_pipeline(self):
        workflow = self.workflow_var.get()
        project = self.current_project
        
        if not workflow:
            messagebox.showerror("Error", "Please select a workflow")
            return
        
        if not project:
            messagebox.showerror("Error", "Please select a project")
            return
        
        files = self.file_drop.get_files()
        
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._run_pipeline_thread, args=(workflow, files, project))
        thread.start()
    
    def _run_pipeline_thread(self, workflow, files, project):
        try:
            workflow_file = f"workflows/{workflow}.yaml"
            self.progress_bar.update_progress(10, "Starting pipeline...")
            self.engine.run_pipeline(workflow_file, input_files=files, project=project)
            self.progress_bar.update_progress(100, "Pipeline completed!")
            messagebox.showinfo("Success", "Pipeline completed successfully")
        except Exception as e:
            self.progress_bar.update_progress(0, "Pipeline failed")
            messagebox.showerror("Error", f"Pipeline failed: {str(e)}")
    
    def validate_workflow(self):
        workflow = self.workflow_var.get()
        if not workflow:
            messagebox.showerror("Error", "Please select a workflow")
            return
        
        try:
            workflow_file = f"workflows/{workflow}.yaml"
            self.engine.validate_workflow(workflow_file)
            messagebox.showinfo("Success", "Workflow is valid")
        except Exception as e:
            messagebox.showerror("Error", f"Workflow validation failed: {str(e)}")
    
    def show_about(self):
        messagebox.showinfo("About", "BioBuntu Studio\nBioinformatics Platform\nVersion 0.1.0")


class ProjectDialog:
    def __init__(self, parent, project_manager):
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Project")
        self.dialog.geometry("400x200")
        self.project_manager = project_manager
        
        ttk.Label(self.dialog, text="Project Name:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10)
        
        ttk.Label(self.dialog, text="Description:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.desc_var = tk.StringVar()
        ttk.Entry(self.dialog, textvariable=self.desc_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10)
        
        button_frame = ttk.Frame(self.dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Create", command=self.create).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy).pack(side=tk.LEFT)
        
        self.dialog.columnconfigure(1, weight=1)
    
    def create(self):
        name = self.name_var.get()
        desc = self.desc_var.get()
        if not name:
            messagebox.showerror("Error", "Project name is required")
            return
        
        try:
            self.project_manager.create_project(name, desc)
            messagebox.showinfo("Success", f"Project '{name}' created successfully")
            self.dialog.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {str(e)}")