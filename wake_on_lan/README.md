# Wake-on-LAN Module for Screen Machine

This module provides Wake-on-LAN functionality to wake up your Ubuntu mini PC from your Windows machine.

## 📁 Directory Structure

```
wake_on_lan/
├── README.md                           # This file - complete documentation
├── config_template.py                  # Configuration template (committed to git)
├── windows/                            # Files for Windows machine (control)
│   ├── README.md                       # Windows-specific instructions
│   ├── wake_on_lan.py                  # Core Wake-on-LAN functionality
│   ├── wake_on_lan_gui.py              # GUI application for Windows
│   └── wake_mini_pc.bat                # Double-click to run GUI
└── ubuntu/                             # Files for Ubuntu machine (target)
    ├── README.md                       # Ubuntu-specific instructions
    └── setup_ubuntu_wol.sh             # Automated setup script for Ubuntu
```

## 🎯 Quick Start

### For Windows Machine (Control)
1. Copy the `windows/` folder to your Windows machine
2. Double-click `wake_mini_pc.bat` to run the GUI
3. Enter your Ubuntu mini PC's MAC address
4. Click "Wake Up Device"

### For Ubuntu Machine (Target)
1. Copy the `ubuntu/` folder to your Ubuntu mini PC
2. Run `chmod +x setup_ubuntu_wol.sh`
3. Run `./setup_ubuntu_wol.sh` to configure Wake-on-LAN
4. Note the MAC address shown by the script

## 🔄 File Transfer Guide

### To Windows Machine
```bash
# Copy these files to your Windows machine:
wake_on_lan/windows/
wake_on_lan/config.py  # (optional - for automatic configuration)
```

### To Ubuntu Machine
```bash
# Copy these files to your Ubuntu mini PC:
wake_on_lan/ubuntu/
```

## ⚙️ Configuration

### Network Configuration (Optional)
You can create a `config.py` file in the `wake_on_lan/` directory to store your network information:

1. **Copy the template:**
   ```bash
   cp wake_on_lan/config_template.py wake_on_lan/config.py
   ```

2. **Edit the configuration:**
   - Replace the MAC address with your Ubuntu mini PC's MAC address
   - Replace the IP addresses with your actual network information
   - Update the network interface name if needed

3. **Security:** The `config.py` file is ignored by git to protect your network information

### Configuration Options
- **MAC Address**: Your Ubuntu mini PC's MAC address
- **IP Address**: Your Ubuntu mini PC's IP address
- **Network Interface**: Your Ubuntu mini PC's network interface (e.g., eth0, enp0s3)
- **Retries**: Number of Wake-on-LAN attempts (default: 3)
- **Delay**: Seconds between attempts (default: 1.0)

## 📋 Prerequisites

### Windows Machine
- Python 3.9+ installed
- Network connectivity to Ubuntu mini PC

### Ubuntu Machine
- Ubuntu 20.04+ (or similar Linux distribution)
- Wake-on-LAN support in BIOS/UEFI
- Network connectivity to Windows machine

## 🔧 Detailed Setup Instructions

### Ubuntu Mini PC Setup

#### Step 1: Enable Wake-on-LAN in BIOS
1. Restart your Ubuntu mini PC
2. Enter BIOS/UEFI (usually F2, F12, or Del)
3. Find "Wake-on-LAN", "Power On by PCI-E", or "Resume by LAN"
4. **Enable** this feature
5. Save and exit BIOS

#### Step 2: Automated Setup (Recommended)
```bash
# Copy the ubuntu folder to your Ubuntu mini PC
# Then run:
chmod +x setup_ubuntu_wol.sh
./setup_ubuntu_wol.sh
```

The script will:
- Detect your network interfaces
- Find your MAC address automatically
- Check Wake-on-LAN support
- Enable Wake-on-LAN
- Create a persistent systemd service
- Test the setup (optional)

#### Step 3: Manual Setup (if script doesn't work)
```bash
# Find your network interface
ip addr show

# Enable Wake-on-LAN (replace eth0 with your interface)
sudo ethtool -s eth0 wol g

# Check if it worked
sudo ethtool eth0 | grep -i wake

# Make it permanent by creating a systemd service
sudo nano /etc/systemd/system/wol.service
```

Add this content (replace `eth0` with your interface):
```ini
[Unit]
Description=Enable Wake On LAN
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/ethtool -s eth0 wol g

[Install]
WantedBy=multi-user.target
```

Then enable it:
```bash
sudo systemctl enable wol.service
sudo systemctl start wol.service
```

### Windows Machine Setup

#### Step 1: Install Python
1. Download Python 3.9+ from [python.org](https://python.org)
2. Make sure to check "Add Python to PATH" during installation

#### Step 2: Copy Files
1. Copy the `windows/` folder to your Windows machine

#### Step 3: Test Installation
```bash
python --version
```

## 🧪 Testing

### Test Locally (on Ubuntu)
```bash
# Install wakeonlan if not already installed
sudo apt install wakeonlan

# Test with your MAC address
sudo wakeonlan [your_mac_address]
```

### Test from Windows
```bash
# Using the GUI (recommended)
# Double-click wake_mini_pc.bat

# Using command line
python wake_on_lan.py [your_mac_address]
```

## 🚨 Troubleshooting

### Common Issues

1. **"Failed to send Wake-on-LAN packet"**
   - Check if Wake-on-LAN is enabled in BIOS
   - Verify network adapter settings on Ubuntu
   - Ensure both devices are on the same network
   - Check firewall settings

2. **"Python is not installed"**
   - Install Python 3.9+ from python.org
   - Make sure Python is added to PATH

3. **"Invalid MAC address format"**
   - Use format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
   - Example: 00:11:22:33:44:55

4. **Ubuntu device doesn't wake up**
   - Verify MAC address is correct
   - Check if device is in sleep/hibernate mode (not powered off)
   - Ensure network cable is connected
   - Try increasing retries and delay
   - Check if Wake-on-LAN is enabled: `sudo ethtool [interface_name] | grep -i wake`

### Ubuntu-Specific Troubleshooting

1. **Check Wake-on-LAN status:**
   ```bash
   sudo ethtool [interface_name] | grep -i wake
   ```

2. **Enable Wake-on-LAN if not enabled:**
   ```bash
   sudo ethtool -s [interface_name] wol g
   ```

3. **Check if the service is running:**
   ```bash
   sudo systemctl status wol-[interface_name].service
   ```

4. **Check network interface status:**
   ```bash
   ip addr show [interface_name]
   ```

### Network Requirements

- Both devices must be on the same local network
- Network must support broadcast packets
- No firewall blocking UDP port 9
- Network switch/router must support Wake-on-LAN

## 🔗 Related Files

This module is part of the larger Screen Machine project. See the main project directory for:
- Product Requirements Document (PRD)
- Initial requirements
- Other modules and components

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Test with a simple ping to ensure network connectivity
4. Check Ubuntu system logs: `journalctl -u wol-[interface_name].service`
5. Check Windows Event Viewer for network-related errors
