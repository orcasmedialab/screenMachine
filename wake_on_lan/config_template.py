# Wake-on-LAN Configuration Template
# Copy this file to config.py and replace the placeholder values with your actual network information
# The config.py file is ignored by git to protect your sensitive network information

# Ubuntu Mini PC Configuration
UBUNTU_MINI_PC = {
    "name": "Ubuntu Mini PC",
    "mac_address": "00:11:22:33:44:55",  # Replace with your actual MAC address
    "ip_address": "192.168.1.100",       # Replace with your actual IP address
    "interface": "eth0",                 # Replace with your actual network interface
    "description": "Mini PC connected to TV"
}

# Windows Machine Configuration (optional - for reference)
WINDOWS_MACHINE = {
    "name": "Windows Control PC",
    "ip_address": "192.168.1.50",        # Replace with your actual IP address
    "description": "Windows machine controlling the mini PC"
}

# Network Configuration
NETWORK = {
    "subnet": "192.168.1.0/24",         # Replace with your actual subnet
    "gateway": "192.168.1.1",           # Replace with your actual gateway
    "broadcast": "192.168.1.255"        # Replace with your actual broadcast address
}

# Wake-on-LAN Settings
WOL_SETTINGS = {
    "retries": 3,                       # Number of retry attempts
    "delay": 1.0,                       # Delay between retries in seconds
    "port": 9                           # Standard Wake-on-LAN port
}

# Example usage:
# from config import UBUNTU_MINI_PC
# mac_address = UBUNTU_MINI_PC["mac_address"]
# ip_address = UBUNTU_MINI_PC["ip_address"]
