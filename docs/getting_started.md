# Getting Started with BioBuntu

Welcome to BioBuntu, a comprehensive bioinformatics platform for running complex analysis pipelines.

## Quick Start

1. **Install BioBuntu**:
   ```bash
   pip install biobuntu
   # or from source: pip install -e .
   ```

2. **Create your first project**:
   ```bash
   biobuntu create-project myproject --description "My first analysis"
   ```

3. **Run a pipeline**:
   ```bash
   biobuntu run workflows/rnaseq.yaml --project myproject --input sample.fastq
   ```

4. **Start the web interface**:
   ```bash
   biobuntu web
   ```
   Then open http://localhost:5000

## Prerequisites

- Python 3.8+
- Bioinformatics tools (FastQC, BWA, etc.) for actual pipeline execution
- For GUI: tkinter (usually included with Python)

## Project Structure

When you create a project, BioBuntu automatically creates an organized directory structure:

```
~/biobuntu/projects/myproject/
├── raw_data/     # Input files
├── qc/          # Quality control results
├── processed/   # Intermediate processing files
├── results/     # Final analysis results
├── reports/     # Summary reports
├── logs/        # Execution logs
└── config/      # Project configuration
```

## Interfaces

BioBuntu provides three user interfaces:

- **CLI**: Command-line interface for scripting and automation
- **GUI**: Desktop application (BioBuntu Studio) for interactive use
- **Web**: Browser-based dashboard for remote access and monitoring

Choose the interface that best fits your workflow!