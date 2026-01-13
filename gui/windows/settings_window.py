import tkinter as tk
from tkinter import ttk, filedialog

class SettingsWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title("Settings")
        self.window.geometry("400x300")
        
        # Config file selection
        ttk.Label(self.window, text="Config File:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.config_var = tk.StringVar(value="config.yaml")
        ttk.Entry(self.window, textvariable=self.config_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10)
        ttk.Button(self.window, text="Browse", command=self.browse_config).grid(row=0, column=2, padx=10)
        
        # Threads
        ttk.Label(self.window, text="Max Threads:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.threads_var = tk.IntVar(value=4)
        ttk.Spinbox(self.window, from_=1, to=16, textvariable=self.threads_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10)
        
        # Memory
        ttk.Label(self.window, text="Max Memory (GB):").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.memory_var = tk.IntVar(value=8)
        ttk.Spinbox(self.window, from_=1, to=64, textvariable=self.memory_var).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=10)
        
        # Buttons
        button_frame = ttk.Frame(self.window)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)
        ttk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=self.window.destroy).pack(side=tk.LEFT, padx=10)
        
        self.window.columnconfigure(1, weight=1)
    
    def browse_config(self):
        file = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")])
        if file:
            self.config_var.set(file)
    
    def save_settings(self):
        # Save settings logic here
        print(f"Config: {self.config_var.get()}")
        print(f"Threads: {self.threads_var.get()}")
        print(f"Memory: {self.memory_var.get()} GB")
        self.window.destroy()