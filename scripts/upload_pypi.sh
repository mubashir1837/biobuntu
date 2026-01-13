#!/bin/bash
# BioBuntu PyPI Upload Script

echo "🚀 BioBuntu PyPI Upload"
echo "======================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if packages exist
if [[ ! -f "dist/biobuntu-0.1.0-py3-none-any.whl" ]] || [[ ! -f "dist/biobuntu-0.1.0.tar.gz" ]]; then
    print_error "Distribution packages not found. Run './scripts/build_all.sh' first."
    exit 1
fi

print_info "Found distribution packages:"
ls -lh dist/biobuntu-*.{whl,tar.gz}

echo ""
print_info "Choose upload destination:"
echo "1) Test PyPI (recommended for testing)"
echo "2) Production PyPI"
echo ""

read -p "Enter choice (1 or 2): " choice

case $choice in
    1)
        print_info "Uploading to Test PyPI..."
        twine upload --repository testpypi dist/*
        print_success "Uploaded to Test PyPI!"
        echo ""
        print_info "Test installation:"
        echo "pip install --index-url https://test.pypi.org/simple/ biobuntu"
        ;;
    2)
        print_warning "Uploading to PRODUCTION PyPI..."
        echo "This will make the package available to everyone via 'pip install biobuntu'"
        read -p "Are you sure? (y/N): " confirm
        if [[ $confirm =~ ^[Yy]$ ]]; then
            twine upload dist/*
            print_success "Uploaded to PyPI!"
            echo ""
            print_info "Now available via:"
            echo "pip install biobuntu"
        else
            print_info "Upload cancelled."
        fi
        ;;
    *)
        print_error "Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
print_success "PyPI upload process complete!"
echo ""
echo "📦 Package Information:"
echo "• Name: biobuntu"
echo "• Version: 0.1.0"
echo "• Author: GenomeHouse"
echo "• License: MIT"
echo ""
echo "🔗 Links:"
echo "• PyPI: https://pypi.org/project/biobuntu/"
echo "• Test PyPI: https://test.pypi.org/project/biobuntu/"