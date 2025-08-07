# Ubuntu Files for Wake-on-LAN

This directory contains all the files needed to configure Wake-on-LAN on your Ubuntu mini PC.

## 📁 Files in This Directory

- **`setup_ubuntu_wol.sh`** - Automated setup script for Wake-on-LAN
- **`README.md`** - This file

## 🚀 Quick Start

### Automated Setup (Recommended)
1. Make the script executable:
   ```bash
   chmod +x setup_ubuntu_wol.sh
   ```

2. Run the setup script:
   ```bash
   ./setup_ubuntu_wol.sh
   ```

3. Follow the prompts to:
   - Select your network interface
   - Enable Wake-on-LAN
   - Create persistent configuration
   - Test the setup

### Manual Setup (if script doesn't work)
See the complete instructions in `../README_WakeOnLAN.md`

## 🔧 Prerequisites

1. **Ubuntu 20.04+** (or similar Linux distribution)
2. **Wake-on-LAN support** in BIOS/UEFI
3. **Network connectivity** to your Windows machine
4. **sudo privileges** for network configuration

## 📋 Setup Steps

### Step 1: Enable Wake-on-LAN in BIOS
1. Restart your Ubuntu mini PC
2. Enter BIOS/UEFI (usually F2, F12, or Del)
3. Find "Wake-on-LAN", "Power On by PCI-E", or "Resume by LAN"
4. **Enable** this feature
5. Save and exit BIOS

### Step 2: Run the Setup Script
```bash
# Copy this directory to your Ubuntu mini PC
# Then run:
chmod +x setup_ubuntu_wol.sh
./setup_ubuntu_wol.sh
```

### Step 3: Verify Setup
```bash
# Check Wake-on-LAN status
sudo ethtool [interface_name] | grep -i wake

# Check systemd service
sudo systemctl status wol-[interface_name].service
```

## 🎯 What the Script Does

1. **Detects network interfaces** and lets you choose
2. **Finds MAC address** automatically
3. **Checks Wake-on-LAN support** for your network adapter
4. **Enables Wake-on-LAN** using ethtool
5. **Creates systemd service** for persistence
6. **Tests the setup** (optional)
7. **Displays summary** with MAC address and status

## 🧪 Testing

### Test Locally
```bash
# Install wakeonlan if not already installed
sudo apt install wakeonlan

# Test with your MAC address
sudo wakeonlan [your_mac_address]
```

### Test from Windows
1. Copy the Windows files to your Windows machine
2. Run the GUI application
3. Enter your MAC address
4. Click "Wake Up Device"

## 🚨 Troubleshooting

### Script Fails to Run
- Make sure it's executable: `chmod +x setup_ubuntu_wol.sh`
- Check if running as regular user (not root)
- Verify you have sudo privileges

### Wake-on-LAN Not Working
1. **Check BIOS**: Wake-on-LAN must be enabled in BIOS
2. **Check Interface**: `sudo ethtool [interface_name] | grep -i wake`
3. **Check Service**: `sudo systemctl status wol-[interface_name].service`
4. **Check Network**: Both devices must be on same network
5. **Check Power State**: Device must be in sleep/hibernate, not powered off

### Common Commands
```bash
# Check Wake-on-LAN status
sudo ethtool [interface_name] | grep -i wake

# Check systemd service
sudo systemctl status wol-[interface_name].service

# Check network interface
ip addr show [interface_name]

# Test Wake-on-LAN
sudo wakeonlan [your_mac_address]
```

## 📊 Configuration Details

### Systemd Service
The script creates a service file at `/etc/systemd/system/wol-[interface_name].service` that:
- Runs after network startup
- Enables Wake-on-LAN for your interface
- Persists across reboots

### Network Interface
The script automatically detects and configures your network interface. Common interface names:
- `eth0` - Traditional Ethernet
- `enp0s3` - Predictable network interface naming
- `wlan0` - Wireless (Wake-on-LAN may not work)

## 🔗 Related Files

- **`wake_on_lan.py`** - Core functionality (copy from parent directory)
- **Windows setup** - See `../windows/` directory
- **Complete docs** - See `../README_WakeOnLAN.md`
- **Quick reference** - See `../UBUNTU_SETUP_QUICK_REFERENCE.md`

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run the setup script with verbose output
3. Check Ubuntu system logs: `journalctl -u wol-[interface_name].service`
4. Verify network connectivity: `ping [windows_ip]`
5. Check the complete documentation in `../README_WakeOnLAN.md`
