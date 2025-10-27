#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

echo "Word Clipper - Starting..."
echo ""

# Try to find a working Python with tkinter
PYTHON_CMD=""

# Try Homebrew Python first (best tkinter support on Mac)
if [ -f "/opt/homebrew/bin/python3" ]; then
    echo "✓ Found Homebrew Python"
    PYTHON_CMD="/opt/homebrew/bin/python3"
elif [ -f "/usr/local/bin/python3" ]; then
    echo "✓ Found Homebrew Python (Intel Mac)"
    PYTHON_CMD="/usr/local/bin/python3"
else
    echo "⚠ Homebrew Python not found, trying system Python..."
    PYTHON_CMD="python3"
fi

# Run the Python script
$PYTHON_CMD content_finder.py

EXIT_CODE=$?

# Keep terminal open to see any messages
echo ""
if [ $EXIT_CODE -ne 0 ]; then
    echo "====================================="
    echo "The application encountered an error."
    echo "====================================="
fi
echo ""
echo "Press any key to exit..."
read -n 1 -s

