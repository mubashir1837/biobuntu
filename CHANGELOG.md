# Changelog

All notable changes to BioBuntu will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-13

### Added
- Stable 1.0.0 release: consolidated and stabilized core features (CLI, GUI, Web, workflows), packaging, and tests.

### Changed
- Bumped package version to **1.0.0**

### Fixed
- Minor bug fixes and test improvements

---

## [0.1.0] - 2024-01-13

### Added
- **Core Engine**: Pipeline execution engine with dependency resolution and parallel processing
- **Project Management**: Create, list, and manage bioinformatics projects with organized directory structures
- **CLI Interface**: Command-line interface with 8 commands for complete workflow management
- **GUI Application**: BioBuntu Studio desktop application with drag-and-drop file input and progress tracking
- **Web Dashboard**: Flask-based web interface with project management and remote job execution
- **Remote Lab Support**: API endpoints for remote pipeline execution with webhook callbacks
- **Tool Wrappers**: Integration with FastQC, BWA, GATK, HISAT2, and Samtools
- **Workflow System**: YAML-based pipeline definitions with validation
- **Packaging**: Support for .deb, PPA, and Conda package formats
- **Documentation**: Comprehensive user and developer documentation
- **API**: RESTful API with 10+ endpoints for programmatic access

### Features
- **Advanced Pipelines**: Dependency management, parallel execution, parameterization
- **Multiple Interfaces**: CLI, GUI, and Web access methods
- **Project Organization**: Automated directory structure creation
- **Remote Execution**: Job queuing and monitoring system
- **Cross-Platform**: Linux packaging for Debian, Ubuntu, and Conda

### Technical
- **Architecture**: Modular design with separate core, CLI, GUI, and web components
- **Dependencies**: Python 3.8+, Click, Flask, PyYAML, tkinter
- **Testing**: Unit tests with pytest
- **Code Quality**: PEP 8 compliant with Black formatting
- **Documentation**: Markdown-based docs with API reference

### Changed
- Initial release - no previous versions

### Deprecated
- None

### Removed
- None

### Fixed
- None

### Security
- No authentication implemented (development version)
- Add authentication for production deployments