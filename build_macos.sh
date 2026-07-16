#!/bin/bash
#
# Build macOS .app and .dmg for Pairwise Test Case Generator
#
# Prerequisites:
#   pip install -r requirements.txt
#   pip install pyinstaller
#
# Usage:
#   chmod +x build_macos.sh
#   ./build_macos.sh
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="Pairwise"
APP_DIR="dist/${APP_NAME}.app"
DMG_NAME="${APP_NAME}-macOS.dmg"

echo "=== Step 1: Clean previous builds ==="
rm -rf build dist

echo "=== Step 2: Build .app with PyInstaller (onefile) ==="
export MACOSX_DEPLOYMENT_TARGET=10.13

pyinstaller \
    --windowed \
    --onefile \
    --name "${APP_NAME}" \
    --icon "pairwise.icns" \
    --add-data "pairwise.icns:." \
    --hidden-import PySide6.QtWidgets \
    --hidden-import PySide6.QtCore \
    --hidden-import PySide6.QtGui \
    --hidden-import PySide6.QtNetwork \
    --hidden-import allpairspy \
    main.py

if [ ! -f "dist/${APP_NAME}" ] && [ ! -d "$APP_DIR" ]; then
    echo "ERROR: Build failed. dist/${APP_NAME} or $APP_DIR not found."
    exit 1
fi

echo "=== Step 3: Sign the app (ad-hoc for local distribution) ==="
codesign --deep --force --sign "-" "$APP_DIR" 2>&1 || echo "Warning: codesign failed (non-critical)"

echo "=== Step 4: Create .dmg ==="
rm -f "$DMG_NAME"

echo "Using hdiutil..."
mkdir -p dist/dmg
cp -R "$APP_DIR" "dist/dmg/"
ln -s /Applications "dist/dmg/Applications"
hdiutil create -volname "${APP_NAME}" \
    -srcfolder "dist/dmg" \
    -ov -format UDZO \
    "${DMG_NAME}"
rm -rf dist/dmg

echo ""
echo "=== Build complete! ==="
echo "📦 DMG:  ${DMG_NAME}"
echo "📁 App:  ${APP_DIR}"
echo ""
echo "Size:"
du -sh "$APP_DIR" "$DMG_NAME" 2>/dev/null || du -sh "dist/${APP_NAME}" "$DMG_NAME"