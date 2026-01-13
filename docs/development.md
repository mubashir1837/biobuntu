# Development Guide

Contributing to BioBuntu development.

## Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GenomeHouse/biobuntu.git
   cd biobuntu
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   ```

4. **Install development dependencies**:
   ```bash
   pip install pytest black flake8
   ```

## Project Structure

```
biobuntu/
├── core/              # Core engine and utilities
│   ├── engine.py      # Pipeline execution engine
│   ├── config.py      # Configuration management
│   ├── logger.py      # Logging utilities
│   └── project_manager.py  # Project management
├── cli/               # Command-line interface
│   └── cli.py         # CLI commands
├── gui/               # Desktop GUI application
│   ├── main.py        # GUI entry point
│   ├── windows/       # GUI windows
│   └── widgets/       # GUI components
├── web/               # Web dashboard
│   ├── api.py         # Flask API
│   ├── routes/        # API route handlers
│   ├── templates/     # HTML templates
│   └── static/        # CSS/JS assets
├── tools/             # Bioinformatics tool wrappers
├── workflows/         # Pipeline definitions
├── configs/           # Default configurations
├── scripts/           # Build and utility scripts
├── tests/             # Unit tests
├── docs/              # Documentation
├── bin/               # Executable scripts
├── conda-recipe/      # Conda packaging
└── pyproject.toml     # Python project configuration
```

## Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/my-feature
```

### 2. Make Changes
- Follow PEP 8 style guidelines
- Add tests for new functionality
- Update documentation
- Ensure backward compatibility

### 3. Run Tests
```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_engine.py

# Run with coverage
pytest --cov=biobuntu
```

### 4. Code Quality
```bash
# Format code
black .

# Check style
flake8 .

# Type checking (if using mypy)
mypy .
```

### 5. Update Documentation
- Update README.md for new features
- Update relevant docs in `docs/`
- Update API documentation if endpoints changed

### 6. Commit Changes
```bash
git add .
git commit -m "Add feature: description"
```

### 7. Create Pull Request
Push to your branch and create a PR on GitHub.

## Adding New Features

### New Tool Wrapper
1. Create `tools/newtool.py`:
   ```python
   def run_newtool(input_file, output_file=None):
       # Implementation
       pass
   ```

2. Update `core/engine.py` to load the new tool

3. Add tests in `tests/`

### New Workflow
1. Create `workflows/new_workflow.yaml`:
   ```yaml
   name: New Workflow
   description: Description
   steps:
     - name: step1
       tool: newtool
   ```

2. Test with: `biobuntu validate workflows/new_workflow.yaml`

### New CLI Command
1. Add to `cli/cli.py`:
   ```python
   @main.command()
   def new_command():
       """Command description"""
       # Implementation
   ```

2. Update help text and documentation

### New API Endpoint
1. Add to `web/api.py` or create new route file
2. Update `web/static/js/app.js` for frontend integration
3. Update API documentation

### New GUI Feature
1. Add to appropriate `gui/windows/` or `gui/widgets/` file
2. Update main window if needed
3. Test GUI functionality

## Testing

### Unit Tests
- Place in `tests/` directory
- Name files as `test_*.py`
- Use pytest framework
- Mock external dependencies

### Integration Tests
- Test complete workflows
- Test API endpoints
- Test CLI commands

### GUI Testing
- Manual testing required
- Test on different platforms
- Verify tkinter compatibility

## Packaging

### Building Packages
```bash
# Debian
./scripts/build_deb.sh

# PPA
./scripts/build_ppa.sh

# Conda
./scripts/build_conda.sh
```

### Release Process
1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag
4. Build packages
5. Upload to repositories
6. Update documentation

## Code Style

- **Python**: PEP 8 compliant
- **Formatting**: Use Black
- **Imports**: Group by standard library, third-party, local
- **Docstrings**: Use Google style docstrings
- **Naming**: snake_case for functions/variables, CamelCase for classes

## Contributing Guidelines

- Write clear commit messages
- Keep PRs focused on single features
- Add tests for new code
- Update documentation
- Be respectful and collaborative

## Getting Help

- Check existing issues on GitHub
- Read the documentation in `docs/`
- Ask questions in discussions
- Join our community chat

## License

By contributing, you agree to license your contributions under the MIT License.