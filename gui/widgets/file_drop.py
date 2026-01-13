import tkinter as tk
from tkinter import filedialog, ttk

class FileDrop:
    def __init__(self, parent, callback=None):
        self.parent = parent
        self.callback = callback
        self.frame = ttk.Frame(parent)
        self.label = ttk.Label(self.frame, text="Drop files here or click to select")
        self.label.pack(pady=20)
        self.listbox = tk.Listbox(self.frame, height=5)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.label.bind("<Button-1>", self.select_files)
        self.frame.drop_target_register(tk.DND_FILES)
        self.frame.dnd_bind('<<Drop>>', self.drop_files)
    
    def select_files(self, event):
        files = filedialog.askopenfilenames()
        if files:
            self.add_files(files)
    
    def drop_files(self, event):
        files = self.frame.tk.splitlist(event.data)
        self.add_files(files)
    
    def add_files(self, files):
        for file in files:
            self.listbox.insert(tk.END, file)
        if self.callback:
            self.callback(files)
    
    def get_files(self):
        return list(self.listbox.get(0, tk.END))
    
    def pack(self, **kwargs):
        self.frame.pack(**kwargs)