import tkinter as tk
from tkinter import ttk

class ProgressBar:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.progress = ttk.Progressbar(self.frame, orient="horizontal", mode="determinate")
        self.progress.pack(fill=tk.X, expand=True)
        self.label = ttk.Label(self.frame, text="Progress: 0%")
        self.label.pack()
    
    def update_progress(self, value, text=None):
        self.progress['value'] = value
        if text:
            self.label.config(text=text)
        else:
            self.label.config(text=f"Progress: {int(value)}%")
        self.frame.update_idletasks()
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)