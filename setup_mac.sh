#!/bin/bash

echo "========================================"
echo "Word Clipper - Mac Setup"
echo "========================================"
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✓ Homebrew is installed"
fi

echo ""
echo "Installing required packages..."
echo ""

# Install ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "✓ FFmpeg already installed"
else
    echo "Installing FFmpeg..."
    brew install ffmpeg
fi

# Install python-tk
echo ""
echo "Installing Python tkinter support..."
echo "(This fixes the GUI compatibility issue on Mac)"
brew install python-tk

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Determine which Python to use
if [ -f "/opt/homebrew/bin/python3" ]; then
    PYTHON_CMD="/opt/homebrew/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    PYTHON_CMD="/usr/local/bin/python3"
else
    PYTHON_CMD="python3"
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
$PYTHON_CMD -m pip install --user --break-system-packages -r requirements.txt

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "You can now run Word Clipper by:"
echo "  1. Double-clicking: content_clipper.command"
echo "  2. Or run: ./content_clipper.sh"
echo ""
echo "Press any key to exit..."
read -n 1 -s

