#!/bin/bash
# Ubuntu Wake-on-LAN Setup Script for Screen Machine
# This script helps configure Wake-on-LAN on Ubuntu systems

set -e

echo "=========================================="
echo "Ubuntu Wake-on-LAN Setup for Screen Machine"
echo "=========================================="
echo

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo "This script should not be run as root. Please run as a regular user."
   exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to get network interface
get_network_interface() {
    echo "Available network interfaces:"
    echo "----------------------------"
    ip addr show | grep -E "^[0-9]+:" | awk '{print $2}' | sed 's/://'
    echo
    
    read -p "Enter the network interface name (e.g., eth0, enp0s3): " interface_name
    
    if ! ip addr show "$interface_name" >/dev/null 2>&1; then
        echo "Error: Interface $interface_name not found."
        exit 1
    fi
    
    echo "Selected interface: $interface_name"
}

# Function to get MAC address
get_mac_address() {
    mac_address=$(ip addr show "$interface_name" | grep -o -E '([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}' | head -1)
    if [[ -z "$mac_address" ]]; then
        echo "Error: Could not find MAC address for interface $interface_name"
        exit 1
    fi
    echo "MAC Address: $mac_address"
}

# Function to check Wake-on-LAN support
check_wol_support() {
    echo "Checking Wake-on-LAN support..."
    
    if ! command_exists ethtool; then
        echo "ethtool not found. Installing..."
        sudo apt update
        sudo apt install -y ethtool
    fi
    
    wol_status=$(sudo ethtool "$interface_name" 2>/dev/null | grep -i "supports wake-on" || echo "Not supported")
    echo "Wake-on-LAN support: $wol_status"
    
    if [[ "$wol_status" == *"Not supported"* ]]; then
        echo "Warning: Wake-on-LAN may not be supported by this network adapter."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Function to enable Wake-on-LAN
enable_wol() {
    echo "Enabling Wake-on-LAN..."
    
    # Enable Wake-on-LAN
    sudo ethtool -s "$interface_name" wol g
    
    # Check if it was enabled
    current_wol=$(sudo ethtool "$interface_name" 2>/dev/null | grep -i "wake-on" | head -1)
    echo "Current Wake-on-LAN status: $current_wol"
}

# Function to create systemd service
create_systemd_service() {
    echo "Creating systemd service for persistent Wake-on-LAN..."
    
    service_content="[Unit]
Description=Enable Wake On LAN for $interface_name
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/ethtool -s $interface_name wol g
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target"
    
    echo "$service_content" | sudo tee /etc/systemd/system/wol-$interface_name.service > /dev/null
    
    # Enable and start the service
    sudo systemctl daemon-reload
    sudo systemctl enable wol-$interface_name.service
    sudo systemctl start wol-$interface_name.service
    
    echo "Systemd service created: wol-$interface_name.service"
}

# Function to test Wake-on-LAN
test_wol() {
    echo "Testing Wake-on-LAN functionality..."
    
    if ! command_exists wakeonlan; then
        echo "Installing wakeonlan package..."
        sudo apt update
        sudo apt install -y wakeonlan
    fi
    
    echo "Sending test Wake-on-LAN packet to $mac_address..."
    sudo wakeonlan "$mac_address"
    echo "Test packet sent. Check if your device responds."
}

# Function to display summary
display_summary() {
    echo
    echo "=========================================="
    echo "Setup Summary"
    echo "=========================================="
    echo "Network Interface: $interface_name"
    echo "MAC Address: $mac_address"
    echo "Wake-on-LAN Status: $(sudo ethtool "$interface_name" 2>/dev/null | grep -i "wake-on" | head -1)"
    echo "Systemd Service: wol-$interface_name.service"
    echo
    echo "To test Wake-on-LAN from another machine, use:"
    echo "wakeonlan $mac_address"
    echo "or"
    echo "python wake_on_lan.py $mac_address"
    echo
    echo "Configuration complete!"
}

# Main execution
main() {
    # Check if running on Ubuntu
    if ! command_exists apt; then
        echo "This script is designed for Ubuntu/Debian systems."
        exit 1
    fi
    
    # Get network interface
    get_network_interface
    
    # Get MAC address
    get_mac_address
    
    # Check Wake-on-LAN support
    check_wol_support
    
    # Enable Wake-on-LAN
    enable_wol
    
    # Create systemd service
    create_systemd_service
    
    # Test Wake-on-LAN
    read -p "Would you like to test Wake-on-LAN now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        test_wol
    fi
    
    # Display summary
    display_summary
}

# Run main function
main "$@"
