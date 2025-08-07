# Windows Files for Wake-on-LAN

This directory contains all the files needed to run Wake-on-LAN from your Windows machine to wake up your Ubuntu mini PC.

## 📁 Files in This Directory

- **`wake_on_lan.py`** - Core Wake-on-LAN functionality
- **`wake_on_lan_gui.py`** - GUI application for easy Wake-on-LAN control
- **`wake_mini_pc.bat`** - Windows batch file for one-click execution
- **`README.md`** - This file

## 🚀 Quick Start

### Option 1: GUI (Recommended)
1. Double-click `wake_mini_pc.bat`
2. Enter your Ubuntu mini PC's MAC address
3. Optionally enter a device name (e.g., "Ubuntu Mini PC")
4. Click "Wake Up Device"

### Option 2: Command Line
```bash
# wake_on_lan.py is included in this directory
python wake_on_lan.py 00:11:22:33:44:55
```

## 🔧 Prerequisites

1. **Python 3.9+** installed on Windows
   - Download from [python.org](https://python.org)
   - Make sure to check "Add Python to PATH" during installation

2. **Network connectivity** to your Ubuntu mini PC
   - Both machines must be on the same local network

3. **MAC address** of your Ubuntu mini PC
   - Get this from the Ubuntu setup script or by running `ip addr show` on Ubuntu

## 📋 Setup Steps

1. **Copy files to Windows machine:**
   - Copy this entire `windows/` folder (includes all needed files)

2. **Test Python installation:**
   ```bash
   python --version
   ```

3. **Run the GUI:**
   - Double-click `wake_mini_pc.bat`

## 🎯 Usage

### GUI Interface
- **Device Name**: Optional friendly name (e.g., "Ubuntu Mini PC", "TV Computer")
- **MAC Address**: Required (format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)
- **Retries**: Number of attempts (default: 3)
- **Delay**: Seconds between attempts (default: 1.0)

### Configuration
The GUI automatically saves your settings to `wol_config.json` in the same directory.

## 🚨 Troubleshooting

### "Python is not installed"
- Install Python 3.9+ from python.org
- Make sure Python is added to PATH

### "Failed to send Wake-on-LAN packet"
- Check if Ubuntu mini PC has Wake-on-LAN enabled
- Verify both machines are on the same network
- Check firewall settings
- Ensure MAC address is correct

### "Invalid MAC address format"
- Use format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
- Example: 00:11:22:33:44:55

## 🔗 Related Files

- **Ubuntu setup** - See `../ubuntu/` directory
- **Complete docs** - See `../README.md`

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify Ubuntu mini PC is properly configured
3. Test network connectivity: `ping [ubuntu_ip]`
4. Check Windows Event Viewer for network errors
