#!/bin/bash
# BioBuntu Debian Package Builder

VERSION="0.1.0"
PACKAGE_NAME="biobuntu"
ARCH="all"
MAINTAINER="GenomeHouse <info@genomehouse.com>"
DESCRIPTION="Bioinformatics platform for running pipelines"

# Create package directory structure
PKG_DIR="${PACKAGE_NAME}_${VERSION}_${ARCH}"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/bin"
mkdir -p "$PKG_DIR/usr/lib/$PACKAGE_NAME"
mkdir -p "$PKG_DIR/usr/share/$PACKAGE_NAME"
mkdir -p "$PKG_DIR/usr/share/doc/$PACKAGE_NAME"

# Copy desktop integration files
cp -r deb-build/* "$PKG_DIR/"

# Create desktop file
cat > "$PKG_DIR/usr/share/applications/biobuntu.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=BioBuntu
Comment=Bioinformatics Platform
Exec=biobuntu web
Icon=biobuntu
Terminal=false
Categories=Science;Biology;Education;
Keywords=bioinformatics;genomics;sequencing;pipeline;
StartupWMClass=BioBuntu
EOF

# Copy icon
cp "deb-build/usr/share/icons/hicolor/128x128/apps/biobuntu.svg" "$PKG_DIR/usr/share/icons/hicolor/128x128/apps/"

# Create control file
cat > "$PKG_DIR/DEBIAN/control" << EOF
Package: $PACKAGE_NAME
Version: $VERSION
Architecture: $ARCH
Maintainer: $MAINTAINER
Description: $DESCRIPTION
Depends: python3, python3-pip, python3-yaml, python3-flask
EOF

# Set proper permissions
chmod 755 "$PKG_DIR/DEBIAN"
chmod 644 "$PKG_DIR/DEBIAN/control"

# Create postinst script
cat > "$PKG_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Install Python dependencies
pip3 install -e /usr/lib/biobuntu

# Make executable
chmod +x /usr/bin/biobuntu

# Update desktop database
if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database
fi

# Update icon cache
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor
fi

echo "BioBuntu installed successfully!"
echo "• Launch from Applications menu or run: biobuntu --help"
echo "• Web interface: biobuntu web"
EOF

chmod +x "$PKG_DIR/DEBIAN/postinst"

# Set proper permissions for all files
find "$PKG_DIR" -type f -exec chmod 644 {} \;
find "$PKG_DIR" -type d -exec chmod 755 {} \;
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# Build the package
dpkg-deb --build "$PKG_DIR"

echo "Package built: ${PKG_DIR}.deb"