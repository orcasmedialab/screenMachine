# Screen Machine

A full-screen application manager for automated screen management with multiple widget windows, designed for Ubuntu systems.

## Overview

Screen Machine is a comprehensive dashboard application designed to manage multiple business applications, entertainment content, and productivity tools in a single full-screen interface. The application features a modular widget system that can be easily customized and extended.

## Features

### 🗓️ Calendar Widget
- Monthly calendar view with event highlighting
- Mock events (easily replaceable with Google Calendar API)
- Interactive day selection
- Today's events list
- Navigation between months

### ⚾ Yankees Games Widget
- Recent and upcoming game information
- Game status indicators (Upcoming, Final, etc.)
- Team statistics
- Mock data (easily replaceable with sports API)

### 🛍️ Shopify Orders Widget
- Recent order display with status tracking
- Order details (customer, amount, items, date)
- Store summary statistics
- Mock data (easily replaceable with Shopify API)

### 🔲 Blank Widget
- Placeholder for future functionality
- Customizable for various purposes:
  - Weather information
  - News feeds
  - System monitoring
  - Social media feeds
  - Stock market data
  - Custom business metrics

## Installation (Ubuntu)

### Quick Install
```bash
# Make installation script executable
chmod +x install_ubuntu.sh

# Run installation script
./install_ubuntu.sh
```

### Manual Install
1. **Install system dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-tk python3-venv python3-dev
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Make launcher executable**:
   ```bash
   chmod +x run_screen_machine.sh
   ```

## Usage

### Running the Application

```bash
# Full-screen mode
./run_screen_machine.sh

# Or directly with Python
python3 screen_machine.py

# Demo mode (not full-screen)
python3 demo.py
```

### Controls

- **Full Screen**: Application starts in full-screen mode
- **Exit Full Screen**: Press `Escape` or `F11`
- **Close Application**: Use `Ctrl+C` in terminal or close window

### Widget Interaction

- **Calendar**: Click on dates to view events
- **Navigation**: Use arrow buttons to navigate months
- **Yankees Widget**: View game information and team stats
- **Shopify Widget**: Monitor order status and store metrics
- **Blank Widget**: Click "Customize This Widget" for information

## Ubuntu-Specific Features

### Auto-start Service
The installation script can create a systemd service for automatic startup:
```bash
# Enable auto-start
sudo systemctl enable screen-machine.service

# Start the service
sudo systemctl start screen-machine

# Check status
sudo systemctl status screen-machine
```

### Desktop Shortcut
A desktop shortcut is automatically created during installation for easy access.

### Virtual Environment
A Python virtual environment is created to isolate dependencies.

## Architecture

### Main Application (`screen_machine.py`)
- Full-screen window management
- Grid-based layout system
- Status bar with real-time clock
- Widget initialization and management

### Base Widget System (`widgets/base_widget.py`)
- Consistent styling and behavior
- Title bar with customizable headers
- Content area management
- Refresh capability for all widgets

### Individual Widgets
- **Calendar Widget**: Month view with event management
- **Yankees Widget**: Sports information display
- **Shopify Widget**: Business metrics and orders
- **Blank Widget**: Extensible placeholder

## Customization

### Adding New Widgets

1. Create a new widget class inheriting from `BaseWidget`
2. Implement the `init_content()` method
3. Add the widget to the main application in `screen_machine.py`

### API Integration

The application is designed for easy API integration:

- **Google Calendar**: Replace mock events in `CalendarWidget`
- **Sports API**: Replace mock data in `YankeesWidget`
- **Shopify API**: Replace mock orders in `ShopifyWidget`
- **Custom APIs**: Add new widgets or extend existing ones

### Styling

All widgets use a consistent color scheme:
- Primary: `#2c3e50` (Dark Blue)
- Secondary: `#34495e` (Medium Blue)
- Accent: `#3498db` (Light Blue)
- Success: `#27ae60` (Green)
- Warning: `#f39c12` (Orange)
- Error: `#e74c3c` (Red)

## Future Enhancements

### Phase 2 Features
- Real-time API integrations
- Automated scheduling system
- Multi-screen support
- Remote control capabilities
- Advanced analytics

### Long-term Vision
- Cloud-based management
- AI-powered content optimization
- Mobile app integration
- IoT device support

## File Structure

```
screenMachine/
├── screen_machine.py          # Main application
├── demo.py                    # Demo version (not full-screen)
├── install_ubuntu.sh          # Ubuntu installation script
├── run_screen_machine.sh      # Ubuntu launcher script
├── requirements.txt           # Python dependencies
├── README_Screen_Machine.md  # This file
└── widgets/                  # Widget modules
    ├── __init__.py
    ├── base_widget.py        # Base widget class
    ├── calendar_widget.py    # Calendar functionality
    ├── yankees_widget.py     # Sports information
    ├── shopify_widget.py     # Business metrics
    └── blank_widget.py       # Placeholder widget
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all widget files are in the `widgets/` directory
2. **Display Issues**: Check if tkinter is properly installed (`python3 -c "import tkinter"`)
3. **Full Screen Problems**: Use `Escape` key to toggle full-screen mode
4. **Permission Issues**: Make sure launcher scripts are executable (`chmod +x *.sh`)

### Ubuntu-Specific

1. **Python not found**: Install Python 3 (`sudo apt install python3`)
2. **tkinter missing**: Install tkinter (`sudo apt install python3-tk`)
3. **Display issues**: Ensure X11 forwarding is enabled for remote connections

### Performance

- Application designed for low resource usage
- Widgets refresh on-demand
- Efficient memory management for long-running sessions

## Contributing

1. Follow the existing code structure
2. Maintain consistent styling and behavior
3. Add proper documentation for new features
4. Test on Ubuntu systems

## License

This project is part of the Screen Machine system. See project documentation for licensing details.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code structure
3. Consult the PRD document in the `requirements/` folder
4. Ensure you're running on Ubuntu/Linux

---

**Screen Machine** - Intelligent Screen Management System for Ubuntu
