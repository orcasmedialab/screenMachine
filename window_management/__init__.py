"""
Window Management Module for Screen Machine

This module provides comprehensive window management capabilities for the Screen Machine system
running on Ubuntu. It handles creating, positioning, resizing, and controlling multiple 
application windows automatically.
"""

from .window_manager import WindowManager, Window, WindowState
from .display_manager import DisplayManager, Display
from .application_launcher import ApplicationLauncher, ProcessInfo
from .layout_engine import LayoutEngine
from .config import *

__version__ = "1.0.0"
__author__ = "Screen Machine Team"

__all__ = [
    'WindowManager',
    'Window',
    'WindowState',
    'DisplayManager',
    'Display',
    'ApplicationLauncher',
    'ProcessInfo',
    'LayoutEngine',
]
