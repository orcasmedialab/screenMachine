#!/bin/bash

# Screen Machine Ubuntu Installation Script
echo "=========================================="
echo "  Screen Machine - Ubuntu Installation"
echo "=========================================="
echo ""

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "❌ Error: This script should not be run as root"
   echo "Please run as a regular user (sudo will be used when needed)"
   exit 1
fi

# Check if running on Ubuntu/Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: This script is designed for Ubuntu/Linux only"
    exit 1
fi

echo "✓ Ubuntu/Linux system detected"
echo ""

# Update package list
echo "Updating package list..."
sudo apt update

# Install Python 3 and tkinter
echo "Installing Python 3 and tkinter..."
sudo apt install -y python3 python3-pip python3-tk

# Install additional dependencies
echo "Installing additional dependencies..."
sudo apt install -y python3-venv python3-dev

# Check Python installation
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✓ Python 3 installed: $PYTHON_VERSION"
else
    echo "❌ Error: Python 3 installation failed"
    exit 1
fi

# Check tkinter
echo "Checking tkinter..."
if python3 -c "import tkinter; print('✓ tkinter available')" 2>/dev/null; then
    echo "✓ tkinter is available"
else
    echo "❌ Error: tkinter not available"
    exit 1
fi

# Create virtual environment (optional but recommended)
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment and install requirements
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip

# Install optional dependencies (commented out in requirements.txt)
echo "Installing optional dependencies..."
pip install requests pillow python-dotenv

echo "✓ Dependencies installed"

# Make launcher script executable
echo "Setting up launcher script..."
chmod +x run_screen_machine.sh

# Create desktop shortcut
echo "Creating desktop shortcut..."
DESKTOP_FILE="$HOME/Desktop/Screen Machine.desktop"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Screen Machine
Comment=Full-screen application manager with multiple widgets
Exec=$PWD/run_screen_machine.sh
Icon=applications-system
Terminal=true
Categories=System;Utility;
EOF

chmod +x "$DESKTOP_FILE"
echo "✓ Desktop shortcut created"

# Create systemd service for auto-start (optional)
echo ""
echo "Would you like to create a systemd service for auto-start? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Creating systemd service..."
    
    SERVICE_FILE="/etc/systemd/system/screen-machine.service"
    sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Screen Machine
After=graphical-session.target

[Service]
Type=simple
User=$USER
Environment=DISPLAY=:0
WorkingDirectory=$PWD
ExecStart=$PWD/run_screen_machine.sh
Restart=always
RestartSec=10

[Install]
WantedBy=graphical-session.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable screen-machine.service
    echo "✓ Systemd service created and enabled"
    echo "  To start: sudo systemctl start screen-machine"
    echo "  To stop:  sudo systemctl stop screen-machine"
    echo "  To status: sudo systemctl status screen-machine"
fi

echo ""
echo "=========================================="
echo "  Installation Complete!"
echo "=========================================="
echo ""
echo "Screen Machine has been installed successfully!"
echo ""
echo "To run the application:"
echo "  ./run_screen_machine.sh"
echo ""
echo "Or double-click the desktop shortcut"
echo ""
echo "For development/testing, you can also run:"
echo "  python3 demo.py"
echo ""
echo "The application will start in full-screen mode."
echo "Press Escape or F11 to toggle full-screen."
echo ""
echo "Happy screen managing! 🖥️"
