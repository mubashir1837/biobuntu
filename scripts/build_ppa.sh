#!/bin/bash
# BioBuntu PPA Package Builder

VERSION="0.1.0"
PACKAGE_NAME="biobuntu"
PPA_NAME="ppa:genomehouse/biobuntu"

# Install required tools
sudo apt-get update
sudo apt-get install -y dpkg-dev debhelper dh-python

# Create source package
mkdir -p build/ppa
cd build/ppa

# Copy source
cp -r ../../* .

# Create debian directory
mkdir -p debian
cat > debian/changelog << EOF
biobuntu ($VERSION-1) focal; urgency=medium

  * Initial release

 -- GenomeHouse <info@genomehouse.com>  $(date -R)
EOF

cat > debian/control << EOF
Source: biobuntu
Maintainer: GenomeHouse <info@genomehouse.com>
Section: science
Priority: optional
Build-Depends: debhelper (>= 9), python3, python3-setuptools, python3-pip
Standards-Version: 4.1.4

Package: biobuntu
Architecture: all
Depends: \${python3:Depends}, python3-yaml, python3-flask
Description: Bioinformatics platform for running pipelines
 BioBuntu is a comprehensive platform for bioinformatics analysis
 with CLI, GUI, and web interfaces.
EOF

cat > debian/rules << 'EOF'
#!/usr/bin/make -f

%:
	dh $@ --with python3

override_dh_auto_install:
	python3 setup.py install --root=debian/biobuntu --install-layout=deb
EOF

chmod +x debian/rules

# Build source package
debuild -S -sa

echo "Source package built. Upload to PPA with:"
echo "dput $PPA_NAME biobuntu_${VERSION}-1_source.changes"