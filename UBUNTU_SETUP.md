# Ubuntu Setup Guide for Screen Machine

This guide provides step-by-step instructions for setting up and running Screen Machine on Ubuntu systems.

## Quick Start

### 1. Download and Extract
```bash
# Clone or download the project
cd ~/projects
git clone <repository-url> screenMachine
cd screenMachine
```

### 2. Run Installation Script
```bash
# Make installation script executable
chmod +x install_ubuntu.sh

# Run the installation script
./install_ubuntu.sh
```

The installation script will:
- Install Python 3 and tkinter
- Create a virtual environment
- Install Python dependencies
- Create a desktop shortcut
- Optionally create a systemd service for auto-start

### 3. Launch the Application
```bash
# Full-screen mode
./run_screen_machine.sh

# Or use the production script
./start_screen_machine.sh start
```

## Manual Installation

If you prefer to install manually:

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk python3-venv python3-dev
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Make Scripts Executable
```bash
chmod +x *.sh
```

## Production Deployment

### Using the Production Script
The `start_screen_machine.sh` script provides production-ready functionality:

```bash
# Start the application
./start_screen_machine.sh start

# Check status
./start_screen_machine.sh status

# View logs
./start_screen_machine.sh logs

# Stop the application
./start_screen_machine.sh stop

# Restart the application
./start_screen_machine.sh restart
```

### Systemd Service
Create a systemd service for automatic startup:

```bash
# Create service file
sudo tee /etc/systemd/system/screen-machine.service > /dev/null << EOF
[Unit]
Description=Screen Machine
After=graphical-session.target

[Service]
Type=simple
User=$USER
Environment=DISPLAY=:0
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/start_screen_machine.sh start
Restart=always
RestartSec=10

[Install]
WantedBy=graphical-session.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable screen-machine.service
sudo systemctl start screen-machine.service
```

### Auto-start on Boot
To start automatically when the user logs in:

1. **Using systemd service** (recommended):
   ```bash
   sudo systemctl enable screen-machine.service
   ```

2. **Using desktop autostart**:
   ```bash
   # Create autostart directory
   mkdir -p ~/.config/autostart
   
   # Create desktop entry
   cat > ~/.config/autostart/screen-machine.desktop << EOF
   [Desktop Entry]
   Type=Application
   Name=Screen Machine
   Exec=$(pwd)/start_screen_machine.sh start
   Hidden=false
   NoDisplay=false
   X-GNOME-Autostart-enabled=true
   EOF
   ```

## Configuration

### Ubuntu Configuration File
The `ubuntu_config.py` file contains Ubuntu-specific settings:

```bash
# View current configuration
python3 ubuntu_config.py

# This will show:
# - OS information
# - Desktop environment detection
# - Display configuration
# - Package requirements
```

### Customizing Widgets
Each widget can be customized by editing the corresponding file in the `widgets/` directory:

- **Calendar Widget**: `widgets/calendar_widget.py`
- **Yankees Widget**: `widgets/yankees_widget.py`
- **Shopify Widget**: `widgets/shopify_widget.py`
- **Blank Widget**: `widgets/blank_widget.py`

## Troubleshooting

### Common Issues

1. **Python not found**:
   ```bash
   sudo apt install python3
   ```

2. **tkinter not available**:
   ```bash
   sudo apt install python3-tk
   ```

3. **Permission denied**:
   ```bash
   chmod +x *.sh
   ```

4. **Display issues**:
   ```bash
   # Check display environment
   echo $DISPLAY
   
   # For remote connections, ensure X11 forwarding
   ssh -X user@host
   ```

5. **Application won't start**:
   ```bash
   # Check logs
   ./start_screen_machine.sh logs
   
   # Check status
   ./start_screen_machine.sh status
   ```

### Debug Mode
Run in demo mode to test without full-screen:

```bash
python3 demo.py
```

### Log Files
Application logs are stored in:
- `screen_machine.log` - Application logs
- `start_screen_machine.sh` - Startup script logs

## Performance Optimization

### For Kiosk Mode
To optimize for continuous display:

1. **Disable screen saver**:
   ```bash
   gsettings set org.gnome.desktop.screensaver idle-activation-enabled false
   ```

2. **Disable power management**:
   ```bash
   gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout 0
   gsettings set org.gnome.settings-daemon.plugins.power sleep-inactive-battery-timeout 0
   ```

3. **Auto-hide cursor** (edit `ubuntu_config.py`):
   ```python
   'auto_hide_cursor': True
   ```

### For Remote Management
Enable SSH access for remote management:

```bash
# Install SSH server
sudo apt install openssh-server

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# Configure firewall
sudo ufw allow ssh
```

## Security Considerations

1. **Run as non-root user**: The application should run as a regular user
2. **Limit network access**: Only open necessary ports
3. **Regular updates**: Keep Ubuntu and Python packages updated
4. **Monitor logs**: Regularly check application logs for issues

## Support and Maintenance

### Regular Maintenance
```bash
# Update system packages
sudo apt update && sudo apt upgrade

# Update Python packages
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Check application status
./start_screen_machine.sh status

# View recent logs
./start_screen_machine.sh logs
```

### Backup
Backup important configuration files:
```bash
# Create backup directory
mkdir -p ~/backups/screen-machine

# Backup configuration
cp -r widgets/ ~/backups/screen-machine/
cp *.py ~/backups/screen-machine/
cp *.sh ~/backups/screen-machine/
```

### Updates
To update the application:
1. Stop the current instance
2. Backup current configuration
3. Download new version
4. Restore configuration
5. Restart the application

---

**Screen Machine** - Optimized for Ubuntu Systems
