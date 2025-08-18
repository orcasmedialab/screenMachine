"""
Ubuntu Configuration for Screen Machine
Configuration options specific to Ubuntu systems
"""

import os
import platform

# Ubuntu-specific configuration
UBUNTU_CONFIG = {
    # Display settings
    'display': {
        'fullscreen': True,
        'start_maximized': True,
        'auto_hide_cursor': False,  # Can be enabled for kiosk mode
        'screen_saver_disable': True,  # Disable screen saver
    },
    
    # System integration
    'system': {
        'auto_start': False,  # Set to True to enable auto-start
        'service_name': 'screen-machine',
        'user': os.getenv('USER', 'ubuntu'),
        'display_env': os.getenv('DISPLAY', ':0'),
    },
    
    # Ubuntu-specific paths
    'paths': {
        'desktop': os.path.expanduser('~/Desktop'),
        'config_dir': os.path.expanduser('~/.config/screen-machine'),
        'log_dir': '/var/log/screen-machine',
        'cache_dir': os.path.expanduser('~/.cache/screen-machine'),
    },
    
    # Package management
    'packages': {
        'python_cmd': 'python3',
        'pip_cmd': 'pip3',
        'system_packages': [
            'python3',
            'python3-pip', 
            'python3-tk',
            'python3-venv',
            'python3-dev'
        ],
        'python_packages': [
            'requests>=2.25.0',
            'pillow>=8.0.0',
            'python-dotenv>=0.19.0'
        ]
    },
    
    # Ubuntu desktop environment detection
    'desktop_environment': {
        'gnome': os.path.exists('/usr/bin/gnome-session'),
        'kde': os.path.exists('/usr/bin/startkde'),
        'xfce': os.path.exists('/usr/bin/xfce4-session'),
        'lxde': os.path.exists('/usr/bin/lxsession'),
    }
}

# System information
SYSTEM_INFO = {
    'os': platform.system(),
    'os_version': platform.version(),
    'python_version': platform.python_version(),
    'architecture': platform.architecture()[0],
    'machine': platform.machine(),
    'processor': platform.processor(),
}

def get_ubuntu_config():
    """Get Ubuntu-specific configuration"""
    return UBUNTU_CONFIG

def get_system_info():
    """Get system information"""
    return SYSTEM_INFO

def is_ubuntu():
    """Check if running on Ubuntu"""
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            return 'ubuntu' in content
    except:
        return False

def get_desktop_environment():
    """Get current desktop environment"""
    de = UBUNTU_CONFIG['desktop_environment']
    for env, exists in de.items():
        if exists:
            return env
    return 'unknown'

def get_display_info():
    """Get display information"""
    display = os.getenv('DISPLAY', ':0')
    wayland = os.getenv('WAYLAND_DISPLAY')
    
    return {
        'display': display,
        'wayland': bool(wayland),
        'x11': not bool(wayland) and display != '',
        'remote': ':' in display and display != ':0'
    }

# Configuration validation
def validate_config():
    """Validate Ubuntu configuration"""
    issues = []
    
    if not is_ubuntu():
        issues.append("Not running on Ubuntu - some features may not work")
    
    if not os.path.exists('/usr/bin/python3'):
        issues.append("Python 3 not found - install with: sudo apt install python3")
    
    if not os.path.exists('/usr/bin/python3-tk'):
        issues.append("tkinter not found - install with: sudo apt install python3-tk")
    
    return issues

if __name__ == "__main__":
    print("Ubuntu Configuration for Screen Machine")
    print("=" * 40)
    
    print(f"OS: {SYSTEM_INFO['os']}")
    print(f"Python: {SYSTEM_INFO['python_version']}")
    print(f"Architecture: {SYSTEM_INFO['architecture']}")
    print(f"Ubuntu: {is_ubuntu()}")
    print(f"Desktop Environment: {get_desktop_environment()}")
    
    display_info = get_display_info()
    print(f"Display: {display_info['display']}")
    print(f"Wayland: {display_info['wayland']}")
    print(f"X11: {display_info['x11']}")
    print(f"Remote: {display_info['remote']}")
    
    print("\nConfiguration Validation:")
    issues = validate_config()
    if issues:
        for issue in issues:
            print(f"⚠️  {issue}")
    else:
        print("✓ Configuration looks good!")
