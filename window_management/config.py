"""
Configuration settings for the Window Management module.
"""

import os
from typing import Tuple, Dict, Any

# Display settings
DEFAULT_DISPLAY = ":0"
DEFAULT_SCREEN = 0

# Window defaults
DEFAULT_WINDOW_SIZE = (800, 600)
DEFAULT_WINDOW_POSITION = (0, 0)
MIN_WINDOW_SIZE = (200, 150)
MAX_WINDOW_SIZE = (3840, 2160)  # 4K resolution

# Browser settings
DEFAULT_BROWSER = "firefox"
BROWSER_OPTIONS = {
    "firefox": ["--new-window", "--kiosk"],
    "chromium": ["--new-window", "--kiosk"],
    "google-chrome": ["--new-window", "--kiosk"]
}

# Application paths
APPLICATION_PATHS = {
    "firefox": "/usr/bin/firefox",
    "chromium": "/usr/bin/chromium-browser",
    "google-chrome": "/usr/bin/google-chrome-stable",
    "libreoffice": "/usr/bin/libreoffice",
    "gedit": "/usr/bin/gedit"
}

# Layout algorithms
LAYOUT_ALGORITHMS = {
    "grid": "Grid-based layout",
    "tile": "Tiled layout",
    "cascade": "Cascading layout",
    "custom": "Custom positioning"
}

# HDMI settings
HDMI_PORTS = {
    "hdmi1": "HDMI-A-1",
    "hdmi2": "HDMI-A-2",
    "hdmi3": "HDMI-A-3",
    "hdmi4": "HDMI-A-4"
}

# Environment variables
DISPLAY_VAR = os.getenv("DISPLAY", DEFAULT_DISPLAY)
XAUTHORITY = os.getenv("XAUTHORITY", "")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Window management settings
WINDOW_MANAGEMENT = {
    "auto_arrange": True,
    "snap_to_grid": True,
    "grid_size": 50,
    "window_margin": 10,
    "focus_follows_mouse": False
}

# Performance settings
PERFORMANCE = {
    "max_windows": 20,
    "refresh_rate": 1.0,  # seconds
    "memory_limit": 512,  # MB
    "cpu_limit": 50  # percentage
}
