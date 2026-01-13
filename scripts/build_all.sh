#!/bin/bash
# BioBuntu Distribution Builder
# Builds all distribution packages for BioBuntu

set -e

echo "🚀 Building BioBuntu Distribution Packages"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create dist directory
mkdir -p dist
print_status "Created dist directory"

# Build Python packages
print_status "Building Python packages..."
python -m build --wheel --sdist
print_success "Python packages built"

# Build Debian package
print_status "Building Debian package..."
./scripts/build_deb.sh
mv biobuntu_*.deb dist/
print_success "Debian package built"

# Try to build conda package if conda-build is available
if command -v conda-build &> /dev/null; then
    print_status "Building Conda package..."
    ./scripts/build_conda.sh
    print_success "Conda package built"
else
    print_warning "conda-build not found, skipping conda package"
fi

# Create distribution summary
print_status "Creating distribution summary..."
cat > dist/README.md << 'EOF'
# BioBuntu Distribution Packages

This directory contains all distribution packages for BioBuntu v0.1.0.

## Available Packages

### Python Packages (Cross-platform)
- `biobuntu-0.1.0-py3-none-any.whl` - Python wheel package
- `biobuntu-0.1.0.tar.gz` - Source distribution

### Linux Packages
- `biobuntu_0.1.0_all.deb` - Debian/Ubuntu package

## Installation Instructions

### Using pip (Recommended)
```bash
pip install biobuntu-0.1.0-py3-none-any.whl
```

### From source
```bash
pip install biobuntu-0.1.0.tar.gz
```

### Debian/Ubuntu
```bash
sudo dpkg -i biobuntu_0.1.0_all.deb
sudo apt-get install -f  # Install dependencies
```

### Using conda (if available)
```bash
conda install biobuntu
```

## Getting Started

After installation, run:
```bash
biobuntu --help
```

## Web Interface

Start the web dashboard:
```bash
biobuntu web
```

Access at: http://localhost:5000

## Documentation

See the main README.md for comprehensive documentation.
EOF

print_success "Distribution summary created"

# List all built packages
echo ""
echo "📦 Built Packages:"
echo "=================="
ls -lh dist/

# Calculate total size
TOTAL_SIZE=$(du -sh dist/ | cut -f1)
echo ""
print_success "Total distribution size: $TOTAL_SIZE"

echo ""
print_success "🎉 BioBuntu distribution packages built successfully!"
echo ""
echo "Next steps:"
echo "1. Test the packages on target systems"
echo "2. Upload to package repositories (PyPI, conda-forge, PPA)"
echo "3. Create GitHub release with these packages"
echo "4. Update documentation with installation instructions"