#!/bin/bash
set -e

REPO="LibSkills/libskills-cli"
VERSION="${1:-v0.1.0}"

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$ARCH" in
    x86_64) ARCH="x86_64" ;;
    aarch64|arm64) ARCH="aarch64" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

echo "Installing libskills $VERSION for $OS-$ARCH..."

URL="https://github.com/$REPO/releases/download/$VERSION/libskills-${OS}-${ARCH}"
DEST="/usr/local/bin/libskills"

if [ ! -w /usr/local/bin ]; then
    echo "Need sudo to install to /usr/local/bin"
    sudo curl -fsSL "$URL" -o "$DEST"
    sudo chmod +x "$DEST"
else
    curl -fsSL "$URL" -o "$DEST"
    chmod +x "$DEST"
fi

echo ""
echo "✓ libskills installed to $DEST"
echo ""
echo "Try it:"
echo "  libskills init"
echo "  libskills update"
echo "  libskills search logging"
