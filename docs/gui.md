# GUI (BioBuntu Studio)

BioBuntu Studio is the desktop graphical user interface for interactive bioinformatics analysis.

## Features

- **Project Management**: Create, select, and manage analysis projects
- **Drag-and-Drop Interface**: Easily add input files by dragging and dropping
- **Workflow Selection**: Choose from available analysis pipelines
- **Real-time Progress**: Monitor pipeline execution with progress bars
- **Validation**: Check workflows before running
- **Settings Management**: Configure analysis parameters and preferences

## Getting Started

Launch the GUI with:
```bash
biobuntu gui
```

## Interface Overview

### Project Panel
- Select existing projects from the dropdown
- Create new projects with the "New Project" button
- View project status and metadata

### Workflow Panel
- Browse available analysis pipelines
- Select the appropriate workflow for your data
- Validate workflow structure before execution

### File Input Panel
- Drag and drop input files or use the file browser
- View selected files in the list
- Remove files if needed

### Progress Panel
- Real-time execution progress
- Step-by-step status updates
- Error reporting and troubleshooting

### Menu System

#### File Menu
- **New Project**: Create a new analysis project
- **Open Project**: Refresh project list
- **Exit**: Close the application

#### Tools Menu
- **Settings**: Configure application preferences
- **Validate Workflow**: Check selected workflow for errors

#### Help Menu
- **About**: View application information and version

## Workflow Execution

1. **Select Project**: Choose or create a project
2. **Choose Workflow**: Select the analysis pipeline
3. **Add Files**: Drag and drop input files
4. **Validate**: Check the workflow (recommended)
5. **Run**: Execute the pipeline with progress monitoring

## Settings

Access settings through Tools → Settings:

- **Config File**: Path to configuration file
- **Max Threads**: Number of parallel processing threads
- **Max Memory**: Memory allocation limit
- **Tool Paths**: Custom paths to bioinformatics tools

## Troubleshooting

### Common Issues

**GUI won't start**: Ensure tkinter is installed (`pip install tk`)

**Tools not found**: Check that bioinformatics tools are installed and in PATH

**Progress stuck**: Check logs in the project's `logs/` directory

**Validation errors**: Review workflow YAML syntax and tool parameters

### Logs

GUI operations are logged to the console and project log files. Check:
- Console output for immediate feedback
- `~/biobuntu/projects/project_name/logs/` for detailed execution logs