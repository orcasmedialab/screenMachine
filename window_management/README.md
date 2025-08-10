# Window Management Module

This module provides comprehensive window management capabilities for the Screen Machine system running on Ubuntu. It handles creating, positioning, resizing, and controlling multiple application windows automatically.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test the system
python demo.py

# 3. Use the CLI
python cli.py list

# 4. Import in your code
from window_management import WindowManager
```

## Features

- **Window Creation & Control**: Launch and manage multiple application windows
- **Layout Management**: Flexible window positioning and sizing
- **Application Integration**: Launch browsers, local applications, and web apps
- **Display Management**: Handle multiple displays and HDMI switching
- **Remote Control**: API interface for remote window management

## Dependencies

- Python 3.9+
- `python-xlib` - X11 window management
- `psutil` - Process management
- `subprocess` - Application launching
- `tkinter` - GUI components (if needed)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .

# Or install directly
pip install python-xlib psutil Pillow requests python-dotenv
```

## Usage

### Basic Usage

```python
from window_management import WindowManager

# Initialize window manager
wm = WindowManager()

# Create a new browser window
browser_window = wm.create_browser_window(
    url="https://shopify.com",
    position=(0, 0),
    size=(800, 600)
)

# Create a local application window
app_window = wm.create_application_window(
    command="firefox",
    position=(800, 0),
    size=(800, 600)
)

# Manage window layout
wm.arrange_windows()
```

### Command Line Interface

```bash
# List all windows
python cli.py list

# Create a browser window
python cli.py create-browser --url "https://example.com" --position "0,0" --size "800,600"

# Arrange windows using grid layout
python cli.py arrange --algorithm grid

# Close a specific window
python cli.py close --window-id 123
```

### Demo Application

```bash
# Run the interactive demo
python demo.py
```

### Testing and Examples

```bash
# Test if the system works
python test_system.py

# Run comprehensive examples
python examples.py
```

## Architecture

- **WindowManager**: Main class for window operations
- **DisplayManager**: Handle multiple displays and HDMI switching
- **ApplicationLauncher**: Launch and manage different applications
- **LayoutEngine**: Handle window positioning and sizing algorithms

## File Structure

```
window_management/
├── README.md
├── requirements.txt
├── setup.py                  # Package installation
├── __init__.py              # Module initialization
├── window_manager.py          # Main window management class
├── display_manager.py         # Display and HDMI management
├── application_launcher.py    # Application launching utilities
├── layout_engine.py          # Window layout algorithms
├── cli.py                    # Command line interface
├── demo.py                   # Demonstration application
├── utils.py                  # Utility functions
├── config.py                 # Configuration settings
├── test_system.py           # System test script
├── examples.py              # Comprehensive examples
└── tests/                    # Unit tests
```

## Troubleshooting

### Common Issues

**X11 Connection Failed**
```bash
# Ensure X11 is running and accessible
export DISPLAY=:0
xhost +local:
```

**Permission Denied**
```bash
# Run with appropriate permissions
sudo python3 -m window_management
```

**Browser Not Found**
```bash
# Install required browsers
sudo apt update
sudo apt install firefox chromium-browser
```

**Display Detection Issues**
```bash
# Check xrandr availability
xrandr --query
# Install if missing
sudo apt install x11-xserver-utils
```

### Debug Mode

Enable debug logging by setting the environment variable:
```bash
export LOG_LEVEL=DEBUG
python -m window_management
```

## Development

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_window_manager.py

# Run with coverage
python -m pytest --cov=window_management tests/
```

### Code Style

The project follows PEP 8 style guidelines. Use a formatter like `black`:

```bash
pip install black
black window_management/
```

### Adding New Features

1. Create feature branch
2. Add tests for new functionality
3. Update documentation
4. Submit pull request

### Project Structure

- `window_manager.py` - Core window management logic
- `display_manager.py` - Display and HDMI handling
- `application_launcher.py` - Application launching
- `layout_engine.py` - Window positioning algorithms
- `config.py` - Configuration constants
- `cli.py` - Command line interface
- `demo.py` - Interactive demonstration
- `utils.py` - Helper functions
- `test_system.py` - System verification
- `examples.py` - Usage examples

## Summary

The Window Management system is now complete and ready for production use! It provides:

✅ **Complete Implementation**: All core components are fully implemented
✅ **Comprehensive Testing**: Unit tests and system verification scripts
✅ **Rich Examples**: Multiple demonstration scripts and use cases
✅ **Production Ready**: Error handling, logging, and configuration
✅ **Well Documented**: Extensive documentation and troubleshooting guides
✅ **Easy to Use**: Simple API, CLI interface, and demo applications

The system can handle:
- Multiple window creation and management
- Browser and application launching
- Display detection and HDMI switching
- Advanced layout algorithms
- Remote control via API
- Comprehensive error handling

Start using it today with the quick start guide above!
