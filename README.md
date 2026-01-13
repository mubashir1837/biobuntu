<p align="center">
  <img width="607" height="215" alt="biobuntu" src="https://github.com/user-attachments/assets/0d82cc8f-82ef-468a-b615-4f35a5a141c6" />
</p>



[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A comprehensive bioinformatics platform for running pipelines, with CLI, GUI, and web interfaces.

## Features

- **Project Management**: Create and manage bioinformatics projects with organized directory structures
- **Advanced Pipelines**: Support for complex workflows with dependencies and parallel execution
- **Multiple Interfaces**: CLI, Desktop GUI (BioBuntu Studio), and Web Dashboard
- **Remote Lab Support**: API endpoints for remote pipeline execution with job tracking
- **Packaging**: Available as .deb packages, PPA, and Conda packages
- **Workflow Support**: RNA-seq, variant calling, metagenomics, and QC pipelines
- **Tool Integration**: Wrappers for FastQC, BWA, GATK, HISAT2, Samtools

## 📦 Installation

### From Source
```bash
git clone https://github.com/GenomeHouse/biobuntu.git
cd biobuntu
pip install -e .
```

### Debian/Ubuntu (.deb)
```bash
sudo dpkg -i biobuntu_0.1.0_all.deb
sudo apt-get install -f  # Install dependencies
```

### Ubuntu PPA
```bash
sudo add-apt-repository ppa:genomehouse/biobuntu
sudo apt-get update
sudo apt-get install biobuntu
```

### Conda
```bash
conda install -c genomehouse biobuntu
```

## 🏁 Quick Start

1. **Create a project**:
   ```bash
   biobuntu create-project myproject --description "RNA-seq analysis"
   ```

2. **Run a pipeline**:
   ```bash
   biobuntu run workflows/rnaseq.yaml --project myproject --input sample.fastq
   ```

3. **Start web interface**:
   ```bash
   biobuntu web
   ```
   Open: http://localhost:5000

## 💻 Usage

### CLI Commands

BioBuntu provides a comprehensive CLI with 8 commands:

```bash
biobuntu --help                    # Show all commands
biobuntu create-project <name>     # Create new project
biobuntu list-projects             # List all projects
biobuntu delete-project <name>     # Delete project
biobuntu list                      # List workflows
biobuntu validate <workflow>       # Validate workflow
biobuntu run <workflow> [options]  # Run pipeline
biobuntu web                       # Start web dashboard
biobuntu gui                       # Start GUI application
```

### Web Dashboard

Access the web interface at http://localhost:5000 with features:
- Create and manage projects
- Run pipelines locally or remotely
- Monitor remote jobs with real-time updates
- Download results and intermediate files

### GUI Application

Launch BioBuntu Studio with `biobuntu gui` featuring:
- Project selection and creation
- Drag-and-drop file input
- Real-time progress tracking
- Workflow validation

## 📁 Project Structure

Projects are automatically organized:

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

## 🔬 Advanced Pipelines

### Features
- **Dependencies**: Steps can depend on previous steps
- **Parallel Execution**: Independent steps run concurrently
- **Parameterization**: Configurable tool arguments
- **Validation**: Check workflow structure before execution

### Example Workflow

```yaml
name: RNA-seq Pipeline
description: Complete RNA-seq analysis
steps:
  - name: qc
    tool: fastqc
    args:
      input_file: raw_data/sample.fastq
      output_dir: qc/
  - name: align
    tool: hisat2
    depends_on: [qc]
    args:
      index: genome_index
      input_fastq1: raw_data/sample.fastq
      output_sam: processed/sample.sam
```

## 🌐 Remote Lab Support

### API Endpoints
- `POST /api/remote/run` - Submit remote jobs
- `GET /api/remote/status/<job_id>` - Check job status
- `GET /api/remote/jobs` - List all remote jobs
- Webhook callbacks for job completion

### Example Remote Execution
```python
import requests

# Submit job
response = requests.post('http://localhost:5000/api/remote/run', json={
    'workflow': 'rnaseq.yaml',
    'project': 'myproject',
    'callback_url': 'https://myapp.com/webhook'
})

job_id = response.json()['job_id']
```

## 📚 Documentation

- **[Getting Started](docs/getting_started.md)** - Quick start guide
- **[Pipelines](docs/pipelines.md)** - Pipeline creation and management
- **[GUI Guide](docs/gui.md)** - Desktop application usage
- **[Web Dashboard](docs/web.md)** - Web interface documentation
- **[API Reference](docs/api.md)** - Complete API documentation
- **[Development](docs/development.md)** - Contributing and development guide

## 🛠️ Development

### Prerequisites
- Python 3.8+
- Bioinformatics tools (optional, for testing)

### Setup
```bash
git clone https://github.com/GenomeHouse/biobuntu.git
cd biobuntu
pip install -e .
pip install pytest black flake8  # Development dependencies
```

### Testing
```bash
pytest                    # Run tests
black .                  # Format code
flake8 .                 # Check style
```

### Building Packages
```bash
./scripts/build_deb.sh    # Debian package
./scripts/build_ppa.sh    # PPA package
./scripts/build_conda.sh  # Conda package
```

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](docs/development.md) for details.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python, Flask, Click, and tkinter
- Inspired by bioinformatics community needs
- Thanks to all contributors and users

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/GenomeHouse/biobuntu/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GenomeHouse/biobuntu/discussions)
- **Documentation**: [Full Docs](docs/)

---

**BioBuntu** - Making bioinformatics accessible through modern interfaces and powerful automation.
