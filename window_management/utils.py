"""
Utility functions for the Window Management system.
"""

import os
import sys
import subprocess
import logging
from typing import List, Tuple, Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


def is_ubuntu_system() -> bool:
    """Check if the system is running Ubuntu."""
    try:
        with open('/etc/os-release', 'r') as f:
            content = f.read().lower()
            return 'ubuntu' in content
    except (FileNotFoundError, PermissionError):
        return False


def is_x11_available() -> bool:
    """Check if X11 is available on the system."""
    return os.environ.get('DISPLAY') is not None


def is_wayland_session() -> bool:
    """Check if the system is running Wayland."""
    return os.environ.get('WAYLAND_DISPLAY') is not None


def get_system_info() -> Dict[str, Any]:
    """Get system information relevant to window management."""
    info = {
        'os': 'unknown',
        'display_server': 'unknown',
        'python_version': sys.version,
        'x11_available': is_x11_available(),
        'wayland_session': is_wayland_session()
    }
    
    # Detect OS
    if is_ubuntu_system():
        info['os'] = 'ubuntu'
    elif sys.platform.startswith('linux'):
        info['os'] = 'linux'
    elif sys.platform == 'darwin':
        info['os'] = 'macos'
    elif sys.platform.startswith('win'):
        info['os'] = 'windows'
    
    # Detect display server
    if info['wayland_session']:
        info['display_server'] = 'wayland'
    elif info['x11_available']:
        info['display_server'] = 'x11'
    
    return info


def check_dependencies() -> Dict[str, bool]:
    """Check if required dependencies are available."""
    dependencies = {
        'python-xlib': False,
        'psutil': False,
        'Pillow': False,
        'requests': False,
        'python-dotenv': False
    }
    
    try:
        import Xlib
        dependencies['python-xlib'] = True
    except ImportError:
        pass
    
    try:
        import psutil
        dependencies['psutil'] = True
    except ImportError:
        pass
    
    try:
        import PIL
        dependencies['Pillow'] = True
    except ImportError:
        pass
    
    try:
        import requests
        dependencies['requests'] = True
    except ImportError:
        pass
    
    try:
        import dotenv
        dependencies['python-dotenv'] = True
    except ImportError:
        pass
    
    return dependencies


def install_dependencies() -> bool:
    """Install missing dependencies using pip."""
    missing = []
    dependencies = check_dependencies()
    
    for dep, available in dependencies.items():
        if not available:
            missing.append(dep)
    
    if not missing:
        logger.info("All dependencies are already installed")
        return True
    
    logger.info(f"Installing missing dependencies: {', '.join(missing)}")
    
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + missing)
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        return False


def validate_window_position(position: Tuple[int, int], 
                           max_width: int = 3840, 
                           max_height: int = 2160) -> bool:
    """Validate window position coordinates."""
    x, y = position
    return 0 <= x <= max_width and 0 <= y <= max_height


def validate_window_size(size: Tuple[int, int], 
                        min_width: int = 200, 
                        min_height: int = 150,
                        max_width: int = 3840, 
                        max_height: int = 2160) -> bool:
    """Validate window size dimensions."""
    width, height = size
    return (min_width <= width <= max_width and 
            min_height <= height <= max_height)


def calculate_grid_layout(window_count: int, 
                         display_width: int, 
                         display_height: int,
                         margin: int = 10) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Calculate grid layout for windows."""
    if window_count == 0:
        return {}
    
    # Calculate grid dimensions
    cols = int(window_count ** 0.5)
    rows = (window_count + cols - 1) // cols
    
    # Calculate cell dimensions
    cell_width = (display_width - margin * (cols + 1)) // cols
    cell_height = (display_height - margin * (rows + 1)) // rows
    
    layout = {}
    for i in range(window_count):
        row = i // cols
        col = i % cols
        
        x = margin + col * (cell_width + margin)
        y = margin + row * (cell_height + margin)
        
        layout[i] = ((x, y), (cell_width, cell_height))
    
    return layout


def calculate_tile_layout(window_count: int, 
                         display_width: int, 
                         display_height: int,
                         margin: int = 10) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Calculate tiled layout for windows."""
    if window_count == 0:
        return {}
    
    if window_count == 1:
        return {0: ((margin, margin), (display_width - 2 * margin, display_height - 2 * margin))}
    
    # Split screen into tiles
    if window_count == 2:
        # Side by side
        half_width = (display_width - 3 * margin) // 2
        layout = {
            0: ((margin, margin), (half_width, display_height - 2 * margin)),
            1: ((2 * margin + half_width, margin), (half_width, display_height - 2 * margin))
        }
    elif window_count == 3:
        # Left half + right split
        left_width = (display_width - 3 * margin) // 2
        right_width = left_width
        right_height = (display_height - 3 * margin) // 2
        
        layout = {
            0: ((margin, margin), (left_width, display_height - 2 * margin)),
            1: ((2 * margin + left_width, margin), (right_width, right_height)),
            2: ((2 * margin + left_width, margin + right_height + margin), (right_width, right_height))
        }
    else:
        # Use grid layout for more than 3 windows
        layout = calculate_grid_layout(window_count, display_width, display_height, margin)
    
    return layout


def calculate_cascade_layout(window_count: int, 
                            display_width: int, 
                            display_height: int,
                            offset: int = 30) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Calculate cascading layout for windows."""
    if window_count == 0:
        return {}
    
    base_width = min(800, display_width - 2 * offset)
    base_height = min(600, display_height - 2 * offset)
    
    layout = {}
    for i in range(window_count):
        x = offset * (i + 1)
        y = offset * (i + 1)
        
        # Ensure windows don't go off-screen
        if x + base_width > display_width:
            x = display_width - base_width - offset
        
        if y + base_height > display_height:
            y = display_height - base_height - offset
        
        layout[i] = ((x, y), (base_width, base_height))
    
    return layout


def format_window_info(window, include_metadata: bool = False) -> str:
    """Format window information for display."""
    info = [
        f"ID: {window.id}",
        f"Title: {window.title}",
        f"Application: {window.application}",
        f"Position: {window.position}",
        f"Size: {window.size}",
        f"State: {window.state.value}",
        f"Display: {window.display}"
    ]
    
    if include_metadata and window.metadata:
        info.append(f"Metadata: {window.metadata}")
    
    return "\n".join(info)


def save_window_configuration(windows: List, filename: str) -> bool:
    """Save window configuration to a JSON file."""
    try:
        import json
        
        config = []
        for window in windows:
            window_config = {
                'title': window.title,
                'application': window.application,
                'position': window.position,
                'size': window.size,
                'state': window.state.value,
                'display': window.display,
                'metadata': window.metadata
            }
            config.append(window_config)
        
        with open(filename, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Window configuration saved to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save window configuration: {e}")
        return False


def load_window_configuration(filename: str) -> List[Dict[str, Any]]:
    """Load window configuration from a JSON file."""
    try:
        import json
        
        with open(filename, 'r') as f:
            config = json.load(f)
        
        logger.info(f"Window configuration loaded from {filename}")
        return config
        
    except Exception as e:
        logger.error(f"Failed to load window configuration: {e}")
        return []


def create_desktop_shortcut(name: str, 
                           command: str, 
                           icon: Optional[str] = None,
                           categories: Optional[List[str]] = None) -> bool:
    """Create a desktop shortcut for the window management system."""
    try:
        desktop_dir = Path.home() / "Desktop"
        if not desktop_dir.exists():
            desktop_dir = Path.home() / ".local" / "share" / "applications"
        
        shortcut_path = desktop_dir / f"{name}.desktop"
        
        # Default categories
        if categories is None:
            categories = ["Utility", "System"]
        
        # Create .desktop file
        content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={name}
Comment=Window Management System
Exec={command}
Terminal=false
Categories={';'.join(categories)}
"""
        
        if icon:
            content += f"Icon={icon}\n"
        
        with open(shortcut_path, 'w') as f:
            f.write(content)
        
        # Make executable
        shortcut_path.chmod(0o755)
        
        logger.info(f"Desktop shortcut created: {shortcut_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to create desktop shortcut: {e}")
        return False


def get_system_resources() -> Dict[str, Any]:
    """Get system resource information."""
    resources = {}
    
    try:
        import psutil
        
        # CPU info
        resources['cpu_percent'] = psutil.cpu_percent(interval=1)
        resources['cpu_count'] = psutil.cpu_count()
        
        # Memory info
        memory = psutil.virtual_memory()
        resources['memory_total'] = memory.total
        resources['memory_available'] = memory.available
        resources['memory_percent'] = memory.percent
        
        # Disk info
        disk = psutil.disk_usage('/')
        resources['disk_total'] = disk.total
        resources['disk_free'] = disk.free
        resources['disk_percent'] = disk.percent
        
    except ImportError:
        logger.warning("psutil not available for system resource monitoring")
    
    return resources


def cleanup_temp_files(pattern: str = "window_mgmt_*") -> int:
    """Clean up temporary files created by the window management system."""
    import tempfile
    import glob
    
    temp_dir = tempfile.gettempdir()
    temp_files = glob.glob(os.path.join(temp_dir, pattern))
    
    cleaned_count = 0
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
            cleaned_count += 1
        except OSError:
            pass
    
    if cleaned_count > 0:
        logger.info(f"Cleaned up {cleaned_count} temporary files")
    
    return cleaned_count
