#!/usr/bin/env python3
"""
Comprehensive examples for the Window Management system.
This script demonstrates various use cases and configurations.
"""

import time
import logging
from typing import List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def example_basic_usage():
    """Basic usage example."""
    print("=" * 50)
    print("Basic Usage Example")
    print("=" * 50)
    
    try:
        from window_management import WindowManager
        
        # Initialize window manager
        wm = WindowManager(auto_arrange=False)
        print("✅ Window Manager initialized")
        
        # Create a browser window
        browser_window = wm.create_browser_window(
            url="https://example.com",
            position=(0, 0),
            size=(800, 600)
        )
        print(f"✅ Browser window created: {browser_window.id}")
        
        # Wait a moment for window to appear
        time.sleep(2)
        
        # List all windows
        windows = wm.list_windows()
        print(f"📋 Total windows: {len(windows)}")
        
        # Clean up
        wm.close_window(browser_window.id)
        print("✅ Browser window closed")
        
    except Exception as e:
        print(f"❌ Error in basic usage: {e}")

def example_multiple_windows():
    """Example with multiple windows."""
    print("\n" + "=" * 50)
    print("Multiple Windows Example")
    print("=" * 50)
    
    try:
        from window_management import WindowManager
        
        wm = WindowManager(auto_arrange=False)
        
        # Create multiple browser windows
        urls = [
            "https://google.com",
            "https://github.com",
            "https://stackoverflow.com"
        ]
        
        windows = []
        for i, url in enumerate(urls):
            window = wm.create_browser_window(
                url=url,
                position=(i * 200, i * 100),
                size=(600, 400)
            )
            windows.append(window)
            print(f"✅ Created window {i+1}: {url}")
            time.sleep(1)
        
        print(f"📋 Created {len(windows)} windows")
        
        # Arrange windows in a grid
        wm.arrange_windows(algorithm="grid")
        print("✅ Windows arranged in grid")
        
        # Wait a moment to see the arrangement
        time.sleep(3)
        
        # Close all windows
        for window in windows:
            wm.close_window(window.id)
        print("✅ All windows closed")
        
    except Exception as e:
        print(f"❌ Error in multiple windows: {e}")

def example_display_management():
    """Example of display management."""
    print("\n" + "=" * 50)
    print("Display Management Example")
    print("=" * 50)
    
    try:
        from window_management.display_manager import DisplayManager
        
        dm = DisplayManager()
        
        # Get display information
        displays = dm.list_displays()
        print(f"📺 Found {len(displays)} displays:")
        
        for display in displays:
            print(f"  - {display.name}: {display.resolution} @ {display.refresh_rate}Hz")
            if display.is_primary:
                print("    (Primary)")
        
        # Get optimal layout area
        area = dm.get_optimal_layout_area()
        print(f"🎯 Optimal layout area: {area}")
        
        # Get primary display
        primary = dm.get_primary_display()
        if primary:
            print(f"⭐ Primary display: {primary.name}")
        
    except Exception as e:
        print(f"❌ Error in display management: {e}")

def example_layout_algorithms():
    """Example of different layout algorithms."""
    print("\n" + "=" * 50)
    print("Layout Algorithms Example")
    print("=" * 50)
    
    try:
        from window_management.layout_engine import LayoutEngine
        
        le = LayoutEngine()
        
        # Define some window positions and sizes
        windows = [
            {"position": (0, 0), "size": (800, 600)},
            {"position": (800, 0), "size": (800, 600)},
            {"position": (0, 600), "size": (800, 600)},
            {"position": (800, 600), "size": (800, 600)}
        ]
        
        # Test different layout algorithms
        algorithms = ["grid", "tile", "cascade"]
        
        for algorithm in algorithms:
            print(f"\n🔄 Testing {algorithm} layout:")
            try:
                arranged = le.arrange_windows(windows, algorithm)
                print(f"  ✅ {algorithm} layout applied")
                for i, window in enumerate(arranged):
                    print(f"    Window {i+1}: {window['position']} {window['size']}")
            except Exception as e:
                print(f"  ❌ {algorithm} layout failed: {e}")
        
    except Exception as e:
        print(f"❌ Error in layout algorithms: {e}")

def example_application_launcher():
    """Example of application launching."""
    print("\n" + "=" * 50)
    print("Application Launcher Example")
    print("=" * 50)
    
    try:
        from window_management.application_launcher import ApplicationLauncher
        
        al = ApplicationLauncher()
        
        # Check available browsers
        browsers = ["firefox", "chromium", "google-chrome"]
        
        for browser in browsers:
            if al.is_browser_available(browser):
                print(f"✅ {browser} is available")
            else:
                print(f"❌ {browser} is not available")
        
        # Check available applications
        apps = ["gedit", "libreoffice", "firefox"]
        
        for app in apps:
            if al.is_application_available(app):
                print(f"✅ {app} is available")
            else:
                print(f"❌ {app} is not available")
        
    except Exception as e:
        print(f"❌ Error in application launcher: {e}")

def example_error_handling():
    """Example of error handling."""
    print("\n" + "=" * 50)
    print("Error Handling Example")
    print("=" * 50)
    
    try:
        from window_management import WindowManager
        
        wm = WindowManager()
        
        # Try to create a window with invalid parameters
        try:
            invalid_window = wm.create_browser_window(
                url="",  # Invalid URL
                position=(-1000, -1000),  # Invalid position
                size=(0, 0)  # Invalid size
            )
        except Exception as e:
            print(f"✅ Caught expected error: {e}")
        
        # Try to close a non-existent window
        try:
            result = wm.close_window(99999)
            if not result:
                print("✅ Correctly handled non-existent window")
        except Exception as e:
            print(f"✅ Caught expected error: {e}")
        
    except Exception as e:
        print(f"❌ Error in error handling example: {e}")

def main():
    """Run all examples."""
    print("🚀 Window Management System Examples")
    print("This script demonstrates various features and use cases.")
    print("Make sure you have the required dependencies installed.")
    print("\nPress Enter to continue...")
    input()
    
    examples = [
        example_basic_usage,
        example_multiple_windows,
        example_display_management,
        example_layout_algorithms,
        example_application_launcher,
        example_error_handling
    ]
    
    for example in examples:
        try:
            example()
        except KeyboardInterrupt:
            print("\n⏹️  Example interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Example failed with error: {e}")
        
        print("\nPress Enter to continue to next example...")
        try:
            input()
        except KeyboardInterrupt:
            print("\n⏹️  Examples stopped by user")
            break
    
    print("\n🎉 All examples completed!")
    print("\nTo explore more features:")
    print("1. Run: python demo.py")
    print("2. Try: python cli.py --help")
    print("3. Check the README.md for more information")

if __name__ == "__main__":
    main()
