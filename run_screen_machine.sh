#!/bin/bash

# Screen Machine Launcher Script for Ubuntu
echo "=========================================="
echo "    Screen Machine - Ubuntu Launcher"
echo "=========================================="
echo "Full-screen application manager with multiple widgets"
echo ""

# Check if running on Ubuntu/Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✓ Linux/Ubuntu system detected"
else
    echo "⚠️  Warning: This script is designed for Ubuntu/Linux"
fi

echo ""

# Check for Python 3 (Ubuntu default)
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✓ Python 3 found: $PYTHON_VERSION"
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    echo "✓ Python found: $PYTHON_VERSION"
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found"
    echo ""
    echo "To install Python 3 on Ubuntu:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip python3-tk"
    echo ""
    echo "Or install from source:"
    echo "  sudo apt install build-essential libssl-dev libffi-dev python3-dev"
    echo "  wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz"
    echo "  tar xzf Python-3.9.0.tgz"
    echo "  cd Python-3.9.0"
    echo "  ./configure --enable-optimizations"
    echo "  sudo make altinstall"
    echo ""
    exit 1
fi

# Check if tkinter is available
echo "Checking tkinter availability..."
if $PYTHON_CMD -c "import tkinter; print('✓ tkinter available')" 2>/dev/null; then
    echo "✓ tkinter is available"
else
    echo "❌ Error: tkinter not available"
    echo ""
    echo "To install tkinter on Ubuntu:"
    echo "  sudo apt update"
    echo "  sudo apt install python3-tk"
    echo ""
    exit 1
fi

echo ""
echo "Starting Screen Machine..."
echo "Press Ctrl+C to exit"
echo ""

# Launch the application
$PYTHON_CMD screen_machine.py
