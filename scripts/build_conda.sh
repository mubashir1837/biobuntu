#!/bin/bash
# BioBuntu Conda Package Builder

# Build the conda package
conda build conda-recipe/

# Convert to other platforms (optional)
# conda convert --platform all /path/to/package.tar.bz2 -o output/

echo "Conda package built successfully!"
echo "Install with: conda install biobuntu"