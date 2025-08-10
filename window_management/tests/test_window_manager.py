"""
Unit tests for the WindowManager class.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import time
from typing import Dict, List, Tuple

from ..window_manager import WindowManager, Window, WindowState
from ..display_manager import DisplayManager
from ..application_launcher import ApplicationLauncher
from ..layout_engine import LayoutEngine


class TestWindowManager(unittest.TestCase):
    """Test cases for WindowManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        with patch('window_management.display_manager.DisplayManager'), \
             patch('window_management.application_launcher.ApplicationLauncher'), \
             patch('window_management.layout_engine.LayoutEngine'):
            
            self.wm = WindowManager(auto_arrange=False)
            self.wm.display_manager = Mock(spec=DisplayManager)
            self.wm.app_launcher = Mock(spec=ApplicationLauncher)
            self.wm.layout_engine = Mock(spec=LayoutEngine)
    
    def test_init(self):
        """Test WindowManager initialization."""
        self.assertEqual(len(self.wm.windows), 0)
        self.assertFalse(self.wm.auto_arrange)
        self.assertEqual(self.wm.window_counter, 0)
    
    def test_create_browser_window(self):
        """Test browser window creation."""
        # Mock process
        mock_process = Mock()
        mock_process.pid = 12345
        self.wm.app_launcher.launch_browser.return_value = mock_process
        
        # Mock window info
        self.wm._get_window_info = Mock(return_value={
            'title': 'Test Browser',
            'pid': 12345
        })
        
        # Create browser window
        window = self.wm.create_browser_window(
            url="https://example.com",
            position=(100, 100),
            size=(800, 600)
        )
        
        # Verify
        self.assertIsInstance(window, Window)
        self.assertEqual(window.title, 'Test Browser')
        self.assertEqual(window.position, (100, 100))
        self.assertEqual(window.size, (800, 600))
        self.assertEqual(window.state, WindowState.NORMAL)
        self.assertEqual(len(self.wm.windows), 1)
    
    def test_create_application_window(self):
        """Test application window creation."""
        # Mock process
        mock_process = Mock()
        mock_process.pid = 54321
        self.wm.app_launcher.launch_application.return_value = mock_process
        
        # Mock window info
        self.wm._get_window_info = Mock(return_value={
            'title': 'Test App',
            'pid': 54321
        })
        
        # Create application window
        window = self.wm.create_application_window(
            command="gedit",
            position=(200, 200),
            size=(600, 400)
        )
        
        # Verify
        self.assertIsInstance(window, Window)
        self.assertEqual(window.title, 'Test App')
        self.assertEqual(window.position, (200, 200))
        self.assertEqual(window.size, (600, 400))
        self.assertEqual(window.state, WindowState.NORMAL)
        self.assertEqual(len(self.wm.windows), 1)
    
    def test_close_window(self):
        """Test window closing."""
        # Create a test window
        window = Window(
            id=1,
            title="Test Window",
            application="test",
            position=(0, 0),
            size=(800, 600),
            state=WindowState.NORMAL,
            display=":0",
            created_at=time.time(),
            last_updated=time.time(),
            metadata={}
        )
        self.wm.windows[1] = window
        
        # Mock process termination
        self.wm.app_launcher.terminate_process = Mock(return_value=True)
        
        # Close window
        result = self.wm.close_window(1)
        
        # Verify
        self.assertTrue(result)
        self.assertNotIn(1, self.wm.windows)
        self.wm.app_launcher.terminate_process.assert_called_once_with(1)
    
    def test_set_window_position(self):
        """Test window position setting."""
        # Create a test window
        window = Window(
            id=1,
            title="Test Window",
            application="test",
            position=(0, 0),
            size=(800, 600),
            state=WindowState.NORMAL,
            display=":0",
            created_at=time.time(),
            last_updated=time.time(),
            metadata={}
        )
        self.wm.windows[1] = window
        
        # Mock geometry setting
        self.wm._set_window_geometry = Mock(return_value=True)
        
        # Set position
        result = self.wm.set_window_position(1, (100, 100))
        
        # Verify
        self.assertTrue(result)
        self.assertEqual(window.position, (100, 100))
        self.wm._set_window_geometry.assert_called_once_with(1, (100, 100), (800, 600))
    
    def test_set_window_size(self):
        """Test window size setting."""
        # Create a test window
        window = Window(
            id=1,
            title="Test Window",
            application="test",
            position=(0, 0),
            size=(800, 600),
            state=WindowState.NORMAL,
            display=":0",
            created_at=time.time(),
            last_updated=time.time(),
            metadata={}
        )
        self.wm.windows[1] = window
        
        # Mock geometry setting
        self.wm._set_window_geometry = Mock(return_value=True)
        
        # Set size
        result = self.wm.set_window_size(1, (1024, 768))
        
        # Verify
        self.assertTrue(result)
        self.assertEqual(window.size, (1024, 768))
        self.wm._set_window_geometry.assert_called_once_with(1, (0, 0), (1024, 768))
    
    def test_window_state_management(self):
        """Test window state management methods."""
        # Create a test window
        window = Window(
            id=1,
            title="Test Window",
            application="test",
            position=(0, 0),
            size=(800, 600),
            state=WindowState.NORMAL,
            display=":0",
            created_at=time.time(),
            last_updated=time.time(),
            metadata={}
        )
        self.wm.windows[1] = window
        
        # Mock state setting
        self.wm._set_window_state = Mock(return_value=True)
        
        # Test minimize
        result = self.wm.minimize_window(1)
        self.assertTrue(result)
        self.assertEqual(window.state, WindowState.MINIMIZED)
        
        # Test maximize
        result = self.wm.maximize_window(1)
        self.assertTrue(result)
        self.assertEqual(window.state, WindowState.MAXIMIZED)
        
        # Test restore
        result = self.wm.restore_window(1)
        self.assertTrue(result)
        self.assertEqual(window.state, WindowState.NORMAL)
    
    def test_arrange_windows(self):
        """Test window arrangement."""
        # Create test windows
        for i in range(3):
            window = Window(
                id=i,
                title=f"Window {i}",
                application="test",
                position=(0, 0),
                size=(800, 600),
                state=WindowState.NORMAL,
                display=":0",
                created_at=time.time(),
                last_updated=time.time(),
                metadata={}
            )
            self.wm.windows[i] = window
        
        # Mock display info and layout
        self.wm.display_manager.get_display_info.return_value = {"width": 1920, "height": 1080}
        self.wm.layout_engine.calculate_layout.return_value = {
            0: ((0, 0), (640, 540)),
            1: ((640, 0), (640, 540)),
            2: ((0, 540), (1280, 540))
        }
        
        # Mock position and size setting
        self.wm.set_window_position = Mock(return_value=True)
        self.wm.set_window_size = Mock(return_value=True)
        
        # Arrange windows
        result = self.wm.arrange_windows("grid")
        
        # Verify
        self.assertTrue(result)
        self.wm.layout_engine.calculate_layout.assert_called_once()
        self.assertEqual(self.wm.set_window_position.call_count, 3)
        self.assertEqual(self.wm.set_window_size.call_count, 3)
    
    def test_get_window_info(self):
        """Test getting window information."""
        # Create a test window
        window = Window(
            id=1,
            title="Test Window",
            application="test",
            position=(0, 0),
            size=(800, 600),
            state=WindowState.NORMAL,
            display=":0",
            created_at=time.time(),
            last_updated=time.time(),
            metadata={}
        )
        self.wm.windows[1] = window
        
        # Get window info
        result = self.wm.get_window_info(1)
        
        # Verify
        self.assertEqual(result, window)
        
        # Test non-existent window
        result = self.wm.get_window_info(999)
        self.assertIsNone(result)
    
    def test_list_windows(self):
        """Test listing all windows."""
        # Create test windows
        for i in range(3):
            window = Window(
                id=i,
                title=f"Window {i}",
                application="test",
                position=(0, 0),
                size=(800, 600),
                state=WindowState.NORMAL,
                display=":0",
                created_at=time.time(),
                last_updated=time.time(),
                metadata={}
            )
            self.wm.windows[i] = window
        
        # List windows
        windows = self.wm.list_windows()
        
        # Verify
        self.assertEqual(len(windows), 3)
        self.assertIsInstance(windows[0], Window)
    
    def test_get_window_count(self):
        """Test getting window count."""
        # Initially no windows
        self.assertEqual(self.wm.get_window_count(), 0)
        
        # Add windows
        for i in range(3):
            window = Window(
                id=i,
                title=f"Window {i}",
                application="test",
                position=(0, 0),
                size=(800, 600),
                state=WindowState.NORMAL,
                display=":0",
                created_at=time.time(),
                last_updated=time.time(),
                metadata={}
            )
            self.wm.windows[i] = window
        
        # Check count
        self.assertEqual(self.wm.get_window_count(), 3)
    
    def test_cleanup(self):
        """Test cleanup method."""
        # Create test windows
        for i in range(3):
            window = Window(
                id=i,
                title=f"Window {i}",
                application="test",
                position=(0, 0),
                size=(800, 600),
                state=WindowState.NORMAL,
                display=":0",
                created_at=time.time(),
                last_updated=time.time(),
                metadata={}
            )
            self.wm.windows[i] = window
        
        # Mock close_window
        self.wm.close_window = Mock(return_value=True)
        
        # Cleanup
        self.wm.cleanup()
        
        # Verify
        self.assertEqual(self.wm.close_window.call_count, 3)
        self.assertEqual(len(self.wm.windows), 0)
    
    def test_context_manager(self):
        """Test context manager functionality."""
        # Mock cleanup
        self.wm.cleanup = Mock()
        
        # Use as context manager
        with self.wm as wm:
            self.assertEqual(wm, self.wm)
        
        # Verify cleanup was called
        self.wm.cleanup.assert_called_once()


if __name__ == '__main__':
    unittest.main()
