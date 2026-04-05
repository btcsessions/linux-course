#!/bin/bash
# Convert icon.svg to macOS .icns format
# Run this on your Mac: bash extras/make-icon.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SVG="$SCRIPT_DIR/icon.svg"
ICONSET="$SCRIPT_DIR/CachyCLI.iconset"
ICNS="$SCRIPT_DIR/icon.icns"
APP_ICON="$HOME/Applications/CachyCLI.app/Contents/Resources/icon.icns"

# Check for rsvg-convert or sips
if command -v rsvg-convert &> /dev/null; then
    CONVERTER="rsvg"
elif command -v sips &> /dev/null; then
    CONVERTER="sips"
else
    echo "Install librsvg: brew install librsvg"
    exit 1
fi

mkdir -p "$ICONSET"

# Generate all required icon sizes
sizes=(16 32 64 128 256 512 1024)
for size in "${sizes[@]}"; do
    if [ "$CONVERTER" = "rsvg" ]; then
        rsvg-convert -w "$size" -h "$size" "$SVG" -o "$ICONSET/icon_${size}x${size}.png"
    else
        # Fallback: use sips with a temporary PNG
        if [ ! -f "/tmp/cachycli_1024.png" ]; then
            echo "sips requires a source PNG. Install librsvg: brew install librsvg"
            exit 1
        fi
        sips -z "$size" "$size" /tmp/cachycli_1024.png --out "$ICONSET/icon_${size}x${size}.png" > /dev/null
    fi
done

# Create the properly named iconset files macOS expects
cp "$ICONSET/icon_16x16.png" "$ICONSET/icon_16x16.png"
cp "$ICONSET/icon_32x32.png" "$ICONSET/icon_16x16@2x.png"
cp "$ICONSET/icon_32x32.png" "$ICONSET/icon_32x32.png"
cp "$ICONSET/icon_64x64.png" "$ICONSET/icon_32x32@2x.png"
cp "$ICONSET/icon_128x128.png" "$ICONSET/icon_128x128.png"
cp "$ICONSET/icon_256x256.png" "$ICONSET/icon_128x128@2x.png"
cp "$ICONSET/icon_256x256.png" "$ICONSET/icon_256x256.png"
cp "$ICONSET/icon_512x512.png" "$ICONSET/icon_256x256@2x.png"
cp "$ICONSET/icon_512x512.png" "$ICONSET/icon_512x512.png"
cp "$ICONSET/icon_1024x1024.png" "$ICONSET/icon_512x512@2x.png"

# Convert to .icns
iconutil -c icns "$ICONSET" -o "$ICNS"
rm -rf "$ICONSET"

# Install into the app bundle if it exists
if [ -d "$HOME/Applications/CachyCLI.app" ]; then
    mkdir -p "$HOME/Applications/CachyCLI.app/Contents/Resources"
    cp "$ICNS" "$APP_ICON"
    echo "Icon installed to CachyCLI.app"

    # Update Info.plist to reference the icon
    PLIST="$HOME/Applications/CachyCLI.app/Contents/Info.plist"
    if [ -f "$PLIST" ] && ! grep -q CFBundleIconFile "$PLIST"; then
        sed -i '' 's|</dict>|    <key>CFBundleIconFile</key>\n    <string>icon</string>\n</dict>|' "$PLIST"
    fi

    # Clear icon cache so Dock picks up the new icon
    touch "$HOME/Applications/CachyCLI.app"
    killall Dock 2>/dev/null || true
    echo "Dock refreshed. You should see the new icon."
else
    echo "Icon saved to: $ICNS"
    echo "Create the app bundle first, then re-run this script."
fi
