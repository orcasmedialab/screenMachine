"""
Main Window Manager class for the Screen Machine system.
Handles window creation, positioning, and management on Ubuntu.
"""

import logging
import time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum

from .display_manager import DisplayManager
from .application_launcher import ApplicationLauncher
from .layout_engine import LayoutEngine
from .config import *

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class WindowState(Enum):
    """Window states."""
    NORMAL = "normal"
    MINIMIZED = "minimized"
    MAXIMIZED = "maximized"
    FULLSCREEN = "fullscreen"
    HIDDEN = "hidden"


@dataclass
class Window:
    """Window information container."""
    id: int
    title: str
    application: str
    position: Tuple[int, int]
    size: Tuple[int, int]
    state: WindowState
    display: str
    created_at: float
    last_updated: float
    metadata: Dict[str, Any]


class WindowManager:
    """
    Main window management class for the Screen Machine system.
    """
    
    def __init__(self, auto_arrange: bool = True):
        """
        Initialize the Window Manager.
        
        Args:
            auto_arrange: Whether to automatically arrange windows
        """
        self.display_manager = DisplayManager()
        self.app_launcher = ApplicationLauncher()
        self.layout_engine = LayoutEngine()
        
        self.windows: Dict[int, Window] = {}
        self.auto_arrange = auto_arrange
        self.window_counter = 0
        
        logger.info("Window Manager initialized")
    
    def create_browser_window(self, 
                            url: str, 
                            position: Optional[Tuple[int, int]] = None,
                            size: Optional[Tuple[int, int]] = None,
                            browser: Optional[str] = None) -> Window:
        """
        Create a new browser window with the specified URL.
        
        Args:
            url: URL to open in the browser
            position: Window position (x, y)
            size: Window size (width, height)
            browser: Browser to use (firefox, chromium, chrome)
            
        Returns:
            Window object representing the created window
        """
        try:
            # Set defaults
            position = position or DEFAULT_WINDOW_POSITION
            size = size or DEFAULT_WINDOW_SIZE
            browser = browser or DEFAULT_BROWSER
            
            # Launch browser
            process = self.app_launcher.launch_browser(browser, url)
            
            # Wait for window to appear
            time.sleep(2)
            
            # Get window information
            window_info = self._get_window_info(process.pid)
            
            # Create window object
            window = Window(
                id=self.window_counter,
                title=window_info.get('title', f'Browser - {url}'),
                application=browser,
                position=position,
                size=size,
                state=WindowState.NORMAL,
                display=DISPLAY_VAR,
                created_at=time.time(),
                last_updated=time.time(),
                metadata={'url': url, 'process_id': process.pid}
            )
            
            # Store window
            self.windows[self.window_counter] = window
            self.window_counter += 1
            
            # Position and size window
            self._set_window_geometry(window.id, position, size)
            
            logger.info(f"Created browser window: {window.title}")
            return window
            
        except Exception as e:
            logger.error(f"Failed to create browser window: {e}")
            raise
    
    def create_application_window(self,
                                command: str,
                                position: Optional[Tuple[int, int]] = None,
                                size: Optional[Tuple[int, int]] = None,
                                args: Optional[List[str]] = None) -> Window:
        """
        Create a new application window.
        
        Args:
            command: Application command to run
            position: Window position (x, y)
            size: Window size (width, height)
            args: Additional command line arguments
            
        Returns:
            Window object representing the created window
        """
        try:
            # Set defaults
            position = position or DEFAULT_WINDOW_POSITION
            size = size or DEFAULT_WINDOW_SIZE
            args = args or []
            
            # Launch application
            process = self.app_launcher.launch_application(command, args)
            
            # Wait for window to appear
            time.sleep(2)
            
            # Get window information
            window_info = self._get_window_info(process.pid)
            
            # Create window object
            window = Window(
                id=self.window_counter,
                title=window_info.get('title', f'Application - {command}'),
                application=command,
                position=position,
                size=size,
                state=WindowState.NORMAL,
                display=DISPLAY_VAR,
                created_at=time.time(),
                last_updated=time.time(),
                metadata={'command': command, 'args': args, 'process_id': process.pid}
            )
            
            # Store window
            self.windows[self.window_counter] = window
            self.window_counter += 1
            
            # Position and size window
            self._set_window_geometry(window.id, position, size)
            
            logger.info(f"Created application window: {window.title}")
            return window
            
        except Exception as e:
            logger.error(f"Failed to create application window: {e}")
            raise
    
    def close_window(self, window_id: int) -> bool:
        """
        Close a specific window.
        
        Args:
            window_id: ID of the window to close
            
        Returns:
            True if window was closed successfully
        """
        try:
            if window_id not in self.windows:
                logger.warning(f"Window {window_id} not found")
                return False
            
            window = self.windows[window_id]
            
            # Close the application process
            if 'process_id' in window.metadata:
                self.app_launcher.terminate_process(window.metadata['process_id'])
            
            # Remove from tracking
            del self.windows[window_id]
            
            logger.info(f"Closed window: {window.title}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to close window {window_id}: {e}")
            return False
    
    def set_window_position(self, window_id: int, position: Tuple[int, int]) -> bool:
        """
        Set the position of a specific window.
        
        Args:
            window_id: ID of the window to move
            position: New position (x, y)
            
        Returns:
            True if position was set successfully
        """
        try:
            if window_id not in self.windows:
                return False
            
            window = self.windows[window_id]
            window.position = position
            window.last_updated = time.time()
            
            # Update actual window position
            self._set_window_geometry(window_id, position, window.size)
            
            logger.debug(f"Moved window {window_id} to {position}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set window position: {e}")
            return False
    
    def set_window_size(self, window_id: int, size: Tuple[int, int]) -> bool:
        """
        Set the size of a specific window.
        
        Args:
            window_id: ID of the window to resize
            size: New size (width, height)
            
        Returns:
            True if size was set successfully
        """
        try:
            if window_id not in self.windows:
                return False
            
            # Validate size
            if size[0] < MIN_WINDOW_SIZE[0] or size[1] < MIN_WINDOW_SIZE[1]:
                logger.warning(f"Window size {size} is too small, using minimum")
                size = MIN_WINDOW_SIZE
            
            if size[0] > MAX_WINDOW_SIZE[0] or size[1] > MAX_WINDOW_SIZE[1]:
                logger.warning(f"Window size {size} is too large, using maximum")
                size = MAX_WINDOW_SIZE
            
            window = self.windows[window_id]
            window.size = size
            window.last_updated = time.time()
            
            # Update actual window size
            self._set_window_geometry(window_id, window.position, size)
            
            logger.debug(f"Resized window {window_id} to {size}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set window size: {e}")
            return False
    
    def minimize_window(self, window_id: int) -> bool:
        """Minimize a specific window."""
        return self._set_window_state(window_id, WindowState.MINIMIZED)
    
    def maximize_window(self, window_id: int) -> bool:
        """Maximize a specific window."""
        return self._set_window_state(window_id, WindowState.MAXIMIZED)
    
    def restore_window(self, window_id: int) -> bool:
        """Restore a window to normal state."""
        return self._set_window_state(window_id, WindowState.NORMAL)
    
    def arrange_windows(self, algorithm: str = "grid") -> bool:
        """
        Arrange all windows using the specified layout algorithm.
        
        Args:
            algorithm: Layout algorithm to use
            
        Returns:
            True if arrangement was successful
        """
        try:
            if not self.windows:
                logger.info("No windows to arrange")
                return True
            
            # Get display information
            display_info = self.display_manager.get_display_info()
            
            # Calculate layout
            layout = self.layout_engine.calculate_layout(
                list(self.windows.values()),
                display_info,
                algorithm
            )
            
            # Apply layout
            for window_id, (position, size) in layout.items():
                if window_id in self.windows:
                    self.set_window_position(window_id, position)
                    self.set_window_size(window_id, size)
            
            logger.info(f"Arranged {len(self.windows)} windows using {algorithm} algorithm")
            return True
            
        except Exception as e:
            logger.error(f"Failed to arrange windows: {e}")
            return False
    
    def get_window_info(self, window_id: int) -> Optional[Window]:
        """Get information about a specific window."""
        return self.windows.get(window_id)
    
    def list_windows(self) -> List[Window]:
        """Get a list of all managed windows."""
        return list(self.windows.values())
    
    def get_window_count(self) -> int:
        """Get the total number of managed windows."""
        return len(self.windows)
    
    def _get_window_info(self, process_id: int) -> Dict[str, Any]:
        """Get window information from X11."""
        # This will be implemented using X11 libraries
        # For now, return basic info
        return {
            'title': f'Process {process_id}',
            'pid': process_id
        }
    
    def _set_window_geometry(self, window_id: int, position: Tuple[int, int], size: Tuple[int, int]) -> bool:
        """Set window geometry using X11."""
        # This will be implemented using X11 libraries
        # For now, just update our tracking
        if window_id in self.windows:
            self.windows[window_id].position = position
            self.windows[window_id].size = size
        return True
    
    def _set_window_state(self, window_id: int, state: WindowState) -> bool:
        """Set window state using X11."""
        try:
            if window_id not in self.windows:
                return False
            
            window = self.windows[window_id]
            window.state = state
            window.last_updated = time.time()
            
            # Update actual window state
            # This will be implemented using X11 libraries
            
            logger.debug(f"Set window {window_id} state to {state.value}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set window state: {e}")
            return False
    
    def cleanup(self):
        """Clean up resources and close all windows."""
        try:
            for window_id in list(self.windows.keys()):
                self.close_window(window_id)
            
            logger.info("Window Manager cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
