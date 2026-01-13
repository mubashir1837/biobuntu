#!/bin/bash
# BioBuntu Installer Script
# Installs BioBuntu from source or packages

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}  BioBuntu Installer v0.1.0${NC}"
    echo -e "${BLUE}================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if running as root for system installation
if [[ $EUID -eq 0 ]]; then
    print_error "Please do not run this script as root"
    exit 1
fi

print_header

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_info "Detected OS: $OS"

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
print_info "Python version: $PYTHON_VERSION"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 first."
    exit 1
fi

print_info "Installing BioBuntu..."

# Install from PyPI (when available) or from local wheel
if [[ -f "dist/biobuntu-0.1.0-py3-none-any.whl" ]]; then
    print_info "Installing from local wheel package..."
    pip3 install --user dist/biobuntu-0.1.0-py3-none-any.whl
elif [[ -f "biobuntu-0.1.0-py3-none-any.whl" ]]; then
    print_info "Installing from wheel package..."
    pip3 install --user biobuntu-0.1.0-py3-none-any.whl
else
    print_info "Installing from source..."
    pip3 install --user -e .
fi

print_success "BioBuntu installed successfully!"

# Add to PATH if needed
SHELL_RC=""
if [[ -n "$ZSH_VERSION" ]]; then
    SHELL_RC="$HOME/.zshrc"
elif [[ -n "$BASH_VERSION" ]]; then
    SHELL_RC="$HOME/.bashrc"
fi

if [[ -n "$SHELL_RC" ]]; then
    if ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$SHELL_RC" 2>/dev/null; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_RC"
        print_info "Added ~/.local/bin to PATH in $SHELL_RC"
        print_info "Please run: source $SHELL_RC"
    fi
fi

echo ""
print_success "Installation complete!"
echo ""
echo "Getting Started:"
echo "================"
echo "• Run: biobuntu --help"
echo "• Start web interface: biobuntu web"
echo "• Create project: biobuntu create-project myproject"
echo ""
echo "Documentation: https://github.com/GenomeHouse/biobuntu"
echo ""
print_info "Enjoy using BioBuntu! 🧬"