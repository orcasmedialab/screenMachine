#!/usr/bin/env python3
"""
Simple test script to verify the window management system works.
Run this to check if all components can be imported and initialized.
"""

import sys
import logging

def test_imports():
    """Test if all modules can be imported."""
    print("Testing imports...")
    
    try:
        from window_management import WindowManager
        print("✅ WindowManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import WindowManager: {e}")
        return False
    
    try:
        from window_management.display_manager import DisplayManager
        print("✅ DisplayManager imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import DisplayManager: {e}")
        return False
    
    try:
        from window_management.application_launcher import ApplicationLauncher
        print("✅ ApplicationLauncher imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import ApplicationLauncher: {e}")
        return False
    
    try:
        from window_management.layout_engine import LayoutEngine
        print("✅ LayoutEngine imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import LayoutEngine: {e}")
        return False
    
    return True

def test_initialization():
    """Test if core classes can be initialized."""
    print("\nTesting initialization...")
    
    try:
        from window_management import WindowManager
        wm = WindowManager()
        print("✅ WindowManager initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize WindowManager: {e}")
        return False
    
    try:
        from window_management.display_manager import DisplayManager
        dm = DisplayManager()
        print("✅ DisplayManager initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize DisplayManager: {e}")
        return False
    
    try:
        from window_management.application_launcher import ApplicationLauncher
        al = ApplicationLauncher()
        print("✅ ApplicationLauncher initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ApplicationLauncher: {e}")
        return False
    
    try:
        from window_management.layout_engine import LayoutEngine
        le = LayoutEngine()
        print("✅ LayoutEngine initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize LayoutEngine: {e}")
        return False
    
    return True

def test_config():
    """Test if configuration is accessible."""
    print("\nTesting configuration...")
    
    try:
        from window_management.config import (
            DEFAULT_WINDOW_SIZE,
            DEFAULT_BROWSER,
            LOG_LEVEL
        )
        print(f"✅ Configuration loaded: {DEFAULT_WINDOW_SIZE}, {DEFAULT_BROWSER}, {LOG_LEVEL}")
    except Exception as e:
        print(f"❌ Failed to load configuration: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("🚀 Testing Window Management System")
    print("=" * 40)
    
    # Set logging to ERROR to reduce noise during tests
    logging.basicConfig(level=logging.ERROR)
    
    success = True
    
    if not test_imports():
        success = False
    
    if not test_initialization():
        success = False
    
    if not test_config():
        success = False
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Run: python demo.py")
        print("2. Try: python cli.py list")
        print("3. Import in your code: from window_management import WindowManager")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
