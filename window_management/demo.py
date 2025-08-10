#!/usr/bin/env python3
"""
Demo script for the Window Management system.
This script demonstrates various features of the window management system.
"""

import time
import sys
import logging
from typing import List, Tuple

from .window_manager import WindowManager, WindowState
from .config import *


def setup_logging():
    """Set up logging for the demo."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def demo_basic_operations():
    """Demonstrate basic window operations."""
    print("\n=== Basic Window Operations ===")
    
    with WindowManager(auto_arrange=False) as wm:
        print("1. Creating browser window...")
        browser_window = wm.create_browser_window(
            url="https://www.google.com",
            position=(100, 100),
            size=(800, 600)
        )
        print(f"   Created browser window: {browser_window.id}")
        
        time.sleep(2)
        
        print("2. Creating application window...")
        app_window = wm.create_application_window(
            command="gedit",
            position=(900, 100),
            size=(600, 400)
        )
        print(f"   Created application window: {app_window.id}")
        
        time.sleep(2)
        
        print("3. Listing all windows...")
        windows = wm.list_windows()
        print(f"   Total windows: {len(windows)}")
        for window in windows:
            print(f"     - {window.id}: {window.title} ({window.application})")
        
        time.sleep(2)
        
        print("4. Modifying window properties...")
        wm.set_window_position(browser_window.id, (200, 200))
        wm.set_window_size(browser_window.id, (900, 700))
        print(f"   Modified browser window position and size")
        
        time.sleep(2)
        
        print("5. Window state management...")
        wm.minimize_window(app_window.id)
        print(f"   Minimized application window")
        
        time.sleep(1)
        
        wm.restore_window(app_window.id)
        print(f"   Restored application window")
        
        time.sleep(2)
        
        print("6. Closing windows...")
        wm.close_window(browser_window.id)
        wm.close_window(app_window.id)
        print(f"   Closed all windows")


def demo_layout_algorithms():
    """Demonstrate different layout algorithms."""
    print("\n=== Layout Algorithms Demo ===")
    
    with WindowManager(auto_arrange=False) as wm:
        # Create multiple windows
        urls = [
            "https://www.google.com",
            "https://www.github.com",
            "https://www.stackoverflow.com"
        ]
        
        windows = []
        for i, url in enumerate(urls):
            window = wm.create_browser_window(
                url=url,
                position=(100 * i, 100 * i),
                size=(600, 400)
            )
            windows.append(window)
            time.sleep(1)
        
        print(f"Created {len(windows)} windows for layout demo")
        
        # Test different layout algorithms
        algorithms = ["grid", "tile", "cascade"]
        
        for algorithm in algorithms:
            print(f"\nTesting {algorithm} layout...")
            wm.arrange_windows(algorithm)
            time.sleep(3)
        
        # Clean up
        for window in windows:
            wm.close_window(window.id)
        print("Cleaned up layout demo windows")


def demo_multiple_displays():
    """Demonstrate multi-display functionality."""
    print("\n=== Multi-Display Demo ===")
    
    with WindowManager(auto_arrange=False) as wm:
        # Get display information
        display_info = wm.display_manager.get_display_info()
        print(f"Display information: {display_info}")
        
        # Create windows on different displays if available
        displays = wm.display_manager.list_displays()
        print(f"Available displays: {len(displays)}")
        
        for i, display in enumerate(displays[:2]):  # Limit to 2 displays for demo
            print(f"Creating window on display {display.name}...")
            window = wm.create_browser_window(
                url=f"https://www.example{i+1}.com",
                position=(100, 100),
                size=(800, 600)
            )
            # Set display for the window
            window.display = display.name
            print(f"   Created window {window.id} on {display.name}")
            time.sleep(2)
        
        # List windows by display
        windows = wm.list_windows()
        for window in windows:
            print(f"   Window {window.id}: {window.title} on {window.display}")
        
        # Clean up
        for window in windows:
            wm.close_window(window.id)
        print("Cleaned up multi-display demo")


def demo_performance_monitoring():
    """Demonstrate performance monitoring features."""
    print("\n=== Performance Monitoring Demo ===")
    
    with WindowManager(auto_arrange=False) as wm:
        # Create multiple windows to test performance
        print("Creating multiple windows for performance test...")
        windows = []
        
        for i in range(5):
            window = wm.create_browser_window(
                url=f"https://www.example{i+1}.com",
                position=(100 * i, 100 * i),
                size=(400, 300)
            )
            windows.append(window)
            time.sleep(0.5)
        
        print(f"Created {len(windows)} windows")
        
        # Monitor performance
        print(f"Current window count: {wm.get_window_count()}")
        
        # Test memory usage (if available)
        try:
            import psutil
            process = psutil.Process()
            memory_mb = process.memory_info().rss / 1024 / 1024
            print(f"Current memory usage: {memory_mb:.1f} MB")
        except ImportError:
            print("psutil not available for memory monitoring")
        
        # Clean up
        for window in windows:
            wm.close_window(window.id)
        print("Cleaned up performance demo windows")


def demo_error_handling():
    """Demonstrate error handling capabilities."""
    print("\n=== Error Handling Demo ===")
    
    with WindowManager(auto_arrange=False) as wm:
        print("1. Testing invalid window ID...")
        result = wm.get_window_info(99999)
        if result is None:
            print("   ✓ Correctly handled non-existent window")
        
        print("2. Testing invalid position...")
        try:
            wm.set_window_position(99999, (100, 100))
        except Exception as e:
            print(f"   ✓ Correctly handled error: {type(e).__name__}")
        
        print("3. Testing invalid size...")
        try:
            wm.set_window_size(99999, (800, 600))
        except Exception as e:
            print(f"   ✓ Correctly handled error: {type(e).__name__}")
        
        print("4. Testing invalid state change...")
        try:
            wm.minimize_window(99999)
        except Exception as e:
            print(f"   ✓ Correctly handled error: {type(e).__name__}")


def interactive_demo():
    """Interactive demo with user input."""
    print("\n=== Interactive Demo ===")
    
    with WindowManager(auto_arrange=False) as wm:
        while True:
            print("\nAvailable actions:")
            print("1. Create browser window")
            print("2. Create application window")
            print("3. List windows")
            print("4. Arrange windows")
            print("5. Close all windows")
            print("6. Exit")
            
            try:
                choice = input("\nEnter your choice (1-6): ").strip()
                
                if choice == '1':
                    url = input("Enter URL (default: https://www.google.com): ").strip()
                    if not url:
                        url = "https://www.google.com"
                    
                    window = wm.create_browser_window(url=url)
                    print(f"Created browser window: {window.id}")
                
                elif choice == '2':
                    command = input("Enter command (default: gedit): ").strip()
                    if not command:
                        command = "gedit"
                    
                    window = wm.create_application_window(command=command)
                    print(f"Created application window: {window.id}")
                
                elif choice == '3':
                    windows = wm.list_windows()
                    if windows:
                        print(f"\nTotal windows: {len(windows)}")
                        for window in windows:
                            print(f"  {window.id}: {window.title} ({window.application})")
                    else:
                        print("No windows found.")
                
                elif choice == '4':
                    algorithm = input("Enter algorithm (grid/tile/cascade, default: grid): ").strip()
                    if not algorithm:
                        algorithm = "grid"
                    
                    if wm.arrange_windows(algorithm):
                        print(f"Windows arranged using {algorithm} algorithm")
                    else:
                        print("Failed to arrange windows")
                
                elif choice == '5':
                    count = wm.get_window_count()
                    for window_id in list(wm.windows.keys()):
                        wm.close_window(window_id)
                    print(f"Closed {count} windows")
                
                elif choice == '6':
                    print("Exiting interactive demo...")
                    break
                
                else:
                    print("Invalid choice. Please enter 1-6.")
                
            except KeyboardInterrupt:
                print("\nExiting interactive demo...")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main demo function."""
    print("Window Management System Demo")
    print("=" * 40)
    
    setup_logging()
    
    try:
        # Run demos
        demo_basic_operations()
        time.sleep(1)
        
        demo_layout_algorithms()
        time.sleep(1)
        
        demo_multiple_displays()
        time.sleep(1)
        
        demo_performance_monitoring()
        time.sleep(1)
        
        demo_error_handling()
        time.sleep(1)
        
        # Ask if user wants interactive demo
        response = input("\nWould you like to try the interactive demo? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            interactive_demo()
        
        print("\nDemo completed successfully!")
        
    except KeyboardInterrupt:
        print("\nDemo interrupted by user.")
    except Exception as e:
        print(f"Demo failed with error: {e}")
        logging.error(f"Demo error: {e}", exc_info=True)
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
