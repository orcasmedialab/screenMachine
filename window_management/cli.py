#!/usr/bin/env python3
"""
Command-line interface for the Window Management system.
"""

import argparse
import sys
import json
import logging
from typing import List, Tuple, Optional

from .window_manager import WindowManager, WindowState
from .config import *


def parse_position(position_str: str) -> Tuple[int, int]:
    """Parse position string in format 'x,y'."""
    try:
        x, y = map(int, position_str.split(','))
        return (x, y)
    except ValueError:
        raise argparse.ArgumentTypeError("Position must be in format 'x,y' (e.g., '100,200')")


def parse_size(size_str: str) -> Tuple[int, int]:
    """Parse size string in format 'widthxheight'."""
    try:
        width, height = map(int, size_str.split('x'))
        return (width, height)
    except ValueError:
        raise argparse.ArgumentTypeError("Size must be in format 'widthxheight' (e.g., '800x600')")


def create_browser_window(args):
    """Create a browser window."""
    try:
        with WindowManager() as wm:
            window = wm.create_browser_window(
                url=args.url,
                position=args.position,
                size=args.size,
                browser=args.browser
            )
            print(f"Created browser window: {window.id} - {window.title}")
            return True
    except Exception as e:
        print(f"Error creating browser window: {e}")
        return False


def create_application_window(args):
    """Create an application window."""
    try:
        with WindowManager() as wm:
            window = wm.create_application_window(
                command=args.command,
                position=args.position,
                size=args.size,
                args=args.args
            )
            print(f"Created application window: {window.id} - {window.title}")
            return True
    except Exception as e:
        print(f"Error creating application window: {e}")
        return False


def list_windows(args):
    """List all windows."""
    try:
        with WindowManager() as wm:
            windows = wm.list_windows()
            
            if not windows:
                print("No windows found.")
                return True
            
            if args.json:
                # Output as JSON
                windows_data = []
                for window in windows:
                    windows_data.append({
                        'id': window.id,
                        'title': window.title,
                        'application': window.application,
                        'position': window.position,
                        'size': window.size,
                        'state': window.state.value,
                        'display': window.display
                    })
                print(json.dumps(windows_data, indent=2))
            else:
                # Output as table
                print(f"{'ID':<5} {'Title':<30} {'App':<15} {'Position':<15} {'Size':<15} {'State':<10}")
                print("-" * 90)
                for window in windows:
                    print(f"{window.id:<5} {window.title[:29]:<30} {window.application[:14]:<15} "
                          f"{str(window.position):<15} {str(window.size):<15} {window.state.value:<10}")
            
            return True
    except Exception as e:
        print(f"Error listing windows: {e}")
        return False


def close_window(args):
    """Close a window."""
    try:
        with WindowManager() as wm:
            if wm.close_window(args.window_id):
                print(f"Window {args.window_id} closed successfully.")
                return True
            else:
                print(f"Failed to close window {args.window_id}.")
                return False
    except Exception as e:
        print(f"Error closing window: {e}")
        return False


def set_window_position(args):
    """Set window position."""
    try:
        with WindowManager() as wm:
            if wm.set_window_position(args.window_id, args.position):
                print(f"Window {args.window_id} position set to {args.position}.")
                return True
            else:
                print(f"Failed to set position for window {args.window_id}.")
                return False
    except Exception as e:
        print(f"Error setting window position: {e}")
        return False


def set_window_size(args):
    """Set window size."""
    try:
        with WindowManager() as wm:
            if wm.set_window_size(args.window_id, args.size):
                print(f"Window {args.window_id} size set to {args.size}.")
                return True
            else:
                print(f"Failed to set size for window {args.window_id}.")
                return False
    except Exception as e:
        print(f"Error setting window size: {e}")
        return False


def set_window_state(args):
    """Set window state."""
    try:
        with WindowManager() as wm:
            state_map = {
                'normal': WindowState.NORMAL,
                'minimized': WindowState.MINIMIZED,
                'maximized': WindowState.MAXIMIZED,
                'fullscreen': WindowState.FULLSCREEN,
                'hidden': WindowState.HIDDEN
            }
            
            if args.state not in state_map:
                print(f"Invalid state: {args.state}. Valid states: {', '.join(state_map.keys())}")
                return False
            
            state = state_map[args.state]
            
            if args.state == 'minimized':
                success = wm.minimize_window(args.window_id)
            elif args.state == 'maximized':
                success = wm.maximize_window(args.window_id)
            elif args.state == 'normal':
                success = wm.restore_window(args.window_id)
            else:
                print(f"State '{args.state}' not yet implemented.")
                return False
            
            if success:
                print(f"Window {args.window_id} state set to {args.state}.")
                return True
            else:
                print(f"Failed to set state for window {args.window_id}.")
                return False
    except Exception as e:
        print(f"Error setting window state: {e}")
        return False


def arrange_windows(args):
    """Arrange windows using specified algorithm."""
    try:
        with WindowManager() as wm:
            if wm.arrange_windows(args.algorithm):
                print(f"Windows arranged using {args.algorithm} algorithm.")
                return True
            else:
                print(f"Failed to arrange windows using {args.algorithm} algorithm.")
                return False
    except Exception as e:
        print(f"Error arranging windows: {e}")
        return False


def get_window_info(args):
    """Get information about a specific window."""
    try:
        with WindowManager() as wm:
            window = wm.get_window_info(args.window_id)
            
            if not window:
                print(f"Window {args.window_id} not found.")
                return False
            
            if args.json:
                # Output as JSON
                window_data = {
                    'id': window.id,
                    'title': window.title,
                    'application': window.application,
                    'position': window.position,
                    'size': window.size,
                    'state': window.state.value,
                    'display': window.display,
                    'created_at': window.created_at,
                    'last_updated': window.last_updated,
                    'metadata': window.metadata
                }
                print(json.dumps(window_data, indent=2))
            else:
                # Output as formatted text
                print(f"Window Information:")
                print(f"  ID: {window.id}")
                print(f"  Title: {window.title}")
                print(f"  Application: {window.application}")
                print(f"  Position: {window.position}")
                print(f"  Size: {window.size}")
                print(f"  State: {window.state.value}")
                print(f"  Display: {window.display}")
                print(f"  Created: {window.created_at}")
                print(f"  Last Updated: {window.last_updated}")
                if window.metadata:
                    print(f"  Metadata: {window.metadata}")
            
            return True
    except Exception as e:
        print(f"Error getting window info: {e}")
        return False


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Window Management CLI for Screen Machine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create a browser window
  python -m window_management.cli browser --url https://example.com --position 100,100 --size 800x600
  
  # Create an application window
  python -m window_management.cli app --command gedit --position 200,200 --size 600x400
  
  # List all windows
  python -m window_management.cli list
  
  # Close a window
  python -m window_management.cli close --window-id 1
  
  # Arrange windows
  python -m window_management.cli arrange --algorithm grid
        """
    )
    
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Browser window command
    browser_parser = subparsers.add_parser('browser', help='Create a browser window')
    browser_parser.add_argument('--url', required=True, help='URL to open')
    browser_parser.add_argument('--position', type=parse_position, help='Window position (x,y)')
    browser_parser.add_argument('--size', type=parse_size, help='Window size (widthxheight)')
    browser_parser.add_argument('--browser', choices=['firefox', 'chromium', 'chrome'], help='Browser to use')
    browser_parser.set_defaults(func=create_browser_window)
    
    # Application window command
    app_parser = subparsers.add_parser('app', help='Create an application window')
    app_parser.add_argument('--command', required=True, help='Command to execute')
    app_parser.add_argument('--position', type=parse_position, help='Window position (x,y)')
    app_parser.add_argument('--size', type=parse_size, help='Window size (widthxheight)')
    app_parser.add_argument('--args', nargs='*', help='Additional arguments')
    app_parser.set_defaults(func=create_application_window)
    
    # List windows command
    list_parser = subparsers.add_parser('list', help='List all windows')
    list_parser.set_defaults(func=list_windows)
    
    # Close window command
    close_parser = subparsers.add_parser('close', help='Close a window')
    close_parser.add_argument('--window-id', type=int, required=True, help='Window ID to close')
    close_parser.set_defaults(func=close_window)
    
    # Set position command
    pos_parser = subparsers.add_parser('position', help='Set window position')
    pos_parser.add_argument('--window-id', type=int, required=True, help='Window ID')
    pos_parser.add_argument('--position', type=parse_position, required=True, help='New position (x,y)')
    pos_parser.set_defaults(func=set_window_position)
    
    # Set size command
    size_parser = subparsers.add_parser('size', help='Set window size')
    size_parser.add_argument('--window-id', type=int, required=True, help='Window ID')
    size_parser.add_argument('--size', type=parse_size, required=True, help='New size (widthxheight)')
    size_parser.set_defaults(func=set_window_size)
    
    # Set state command
    state_parser = subparsers.add_parser('state', help='Set window state')
    state_parser.add_argument('--window-id', type=int, required=True, help='Window ID')
    state_parser.add_argument('--state', choices=['normal', 'minimized', 'maximized', 'fullscreen', 'hidden'], required=True, help='New state')
    state_parser.set_defaults(func=set_window_state)
    
    # Arrange windows command
    arrange_parser = subparsers.add_parser('arrange', help='Arrange windows')
    arrange_parser.add_argument('--algorithm', choices=['grid', 'tile', 'cascade'], default='grid', help='Layout algorithm')
    arrange_parser.set_defaults(func=arrange_windows)
    
    # Get window info command
    info_parser = subparsers.add_parser('info', help='Get window information')
    info_parser.add_argument('--window-id', type=int, required=True, help='Window ID')
    info_parser.set_defaults(func=get_window_info)
    
    args = parser.parse_args()
    
    # Set up logging
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
    else:
        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    
    # Execute command
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        success = args.func(args)
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
