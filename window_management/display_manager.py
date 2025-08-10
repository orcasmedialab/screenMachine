"""
Display Manager for handling multiple displays and HDMI switching.
"""

import logging
import subprocess
import json
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass

from .config import *

logger = logging.getLogger(__name__)


@dataclass
class Display:
    """Display information container."""
    name: str
    id: str
    resolution: Tuple[int, int]
    refresh_rate: float
    is_primary: bool
    is_active: bool
    hdmi_port: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class DisplayManager:
    """
    Manages display information and HDMI switching for the Screen Machine system.
    """
    
    def __init__(self):
        """Initialize the Display Manager."""
        self.displays: Dict[str, Display] = {}
        self.primary_display: Optional[str] = None
        
        # Initialize displays
        self._refresh_displays()
        logger.info("Display Manager initialized")
    
    def _refresh_displays(self):
        """Refresh display information from the system."""
        try:
            # Get display information using xrandr
            result = subprocess.run(
                ['xrandr', '--query'],
                capture_output=True,
                text=True,
                check=True
            )
            
            self._parse_xrandr_output(result.stdout)
            logger.debug(f"Refreshed {len(self.displays)} displays")
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to get display information: {e}")
        except FileNotFoundError:
            logger.warning("xrandr not found, using fallback display detection")
            self._fallback_display_detection()
    
    def _parse_xrandr_output(self, output: str):
        """Parse xrandr output to extract display information."""
        lines = output.strip().split('\n')
        current_display = None
        
        for line in lines:
            if ' connected ' in line:
                # New display connected
                parts = line.split()
                name = parts[0]
                is_primary = 'primary' in line
                
                # Extract resolution and refresh rate
                resolution = (1920, 1080)  # Default
                refresh_rate = 60.0  # Default
                
                # Look for resolution in the line
                for part in parts:
                    if 'x' in part and part.replace('x', '').replace('.', '').isdigit():
                        try:
                            width, height = part.split('x')
                            resolution = (int(width), int(height))
                        except ValueError:
                            pass
                
                # Create display object
                display = Display(
                    name=name,
                    id=name,
                    resolution=resolution,
                    refresh_rate=refresh_rate,
                    is_primary=is_primary,
                    is_active=True,
                    hdmi_port=self._get_hdmi_port(name),
                    metadata={}
                )
                
                self.displays[name] = display
                current_display = name
                
                if is_primary:
                    self.primary_display = name
                    
            elif current_display and 'x' in line and 'y' in line:
                # Resolution line
                try:
                    parts = line.strip().split()
                    if len(parts) >= 1:
                        res_part = parts[0]
                        if 'x' in res_part:
                            width, height = res_part.split('x')
                            self.displays[current_display].resolution = (int(width), int(height))
                except (ValueError, IndexError):
                    pass
    
    def _fallback_display_detection(self):
        """Fallback display detection when xrandr is not available."""
        # Create a default display
        default_display = Display(
            name=":0.0",
            id=":0.0",
            resolution=(1920, 1080),
            refresh_rate=60.0,
            is_primary=True,
            is_active=True,
            hdmi_port="hdmi1",
            metadata={}
        )
        
        self.displays[":0.0"] = default_display
        self.primary_display = ":0.0"
    
    def _get_hdmi_port(self, display_name: str) -> Optional[str]:
        """Get HDMI port for a display."""
        # This is a simplified mapping
        # In a real implementation, you'd query the actual hardware
        if 'HDMI' in display_name.upper():
            return "hdmi1"
        elif 'DP' in display_name.upper():
            return "displayport1"
        return None
    
    def get_display_info(self) -> Dict[str, Any]:
        """
        Get comprehensive display information.
        
        Returns:
            Dictionary containing display information
        """
        return {
            'displays': {name: {
                'name': display.name,
                'id': display.id,
                'resolution': display.resolution,
                'refresh_rate': display.refresh_rate,
                'is_primary': display.is_primary,
                'is_active': display.is_active,
                'hdmi_port': display.hdmi_port
            } for name, display in self.displays.items()},
            'primary_display': self.primary_display,
            'total_displays': len(self.displays),
            'total_resolution': self._calculate_total_resolution()
        }
    
    def _calculate_total_resolution(self) -> Tuple[int, int]:
        """Calculate total resolution across all displays."""
        if not self.displays:
            return (0, 0)
        
        # For now, return the primary display resolution
        # In a real implementation, you'd calculate the combined resolution
        primary = self.primary_display
        if primary and primary in self.displays:
            return self.displays[primary].resolution
        
        return (1920, 1080)  # Default fallback
    
    def get_primary_display(self) -> Optional[Display]:
        """Get the primary display."""
        if self.primary_display:
            return self.displays.get(self.primary_display)
        return None
    
    def get_display_by_name(self, name: str) -> Optional[Display]:
        """Get a display by name."""
        return self.displays.get(name)
    
    def list_displays(self) -> List[Display]:
        """Get a list of all displays."""
        return list(self.displays.values())
    
    def switch_hdmi_port(self, port: str) -> bool:
        """
        Switch to a specific HDMI port.
        
        Args:
            port: HDMI port to switch to (e.g., 'hdmi1', 'hdmi2')
            
        Returns:
            True if switching was successful
        """
        try:
            if port not in HDMI_PORTS:
                logger.error(f"Invalid HDMI port: {port}")
                return False
            
            # This would typically involve sending commands to the HDMI switch
            # For now, we'll simulate the switch
            logger.info(f"Switching to HDMI port: {port}")
            
            # Update display information
            self._refresh_displays()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to switch HDMI port: {e}")
            return False
    
    def set_display_resolution(self, display_name: str, resolution: Tuple[int, int]) -> bool:
        """
        Set the resolution of a specific display.
        
        Args:
            display_name: Name of the display
            resolution: New resolution (width, height)
            
        Returns:
            True if resolution was set successfully
        """
        try:
            if display_name not in self.displays:
                logger.error(f"Display not found: {display_name}")
                return False
            
            # Validate resolution
            if resolution[0] < 800 or resolution[1] < 600:
                logger.error(f"Resolution too low: {resolution}")
                return False
            
            # Use xrandr to set resolution
            cmd = [
                'xrandr', '--output', display_name,
                '--mode', f"{resolution[0]}x{resolution[1]}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                # Update our tracking
                self.displays[display_name].resolution = resolution
                logger.info(f"Set {display_name} resolution to {resolution}")
                return True
            else:
                logger.error(f"Failed to set resolution: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to set display resolution: {e}")
            return False
    
    def enable_display(self, display_name: str) -> bool:
        """Enable a specific display."""
        try:
            if display_name not in self.displays:
                return False
            
            cmd = ['xrandr', '--output', display_name, '--auto']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.displays[display_name].is_active = True
                logger.info(f"Enabled display: {display_name}")
                return True
            else:
                logger.error(f"Failed to enable display: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to enable display: {e}")
            return False
    
    def disable_display(self, display_name: str) -> bool:
        """Disable a specific display."""
        try:
            if display_name not in self.displays:
                return False
            
            cmd = ['xrandr', '--output', display_name, '--off']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.displays[display_name].is_active = False
                logger.info(f"Disabled display: {display_name}")
                return True
            else:
                logger.error(f"Failed to disable display: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to disable display: {e}")
            return False
    
    def refresh_displays(self):
        """Manually refresh display information."""
        self._refresh_displays()
        logger.info("Display information refreshed")
    
    def get_optimal_layout_area(self) -> Tuple[int, int, int, int]:
        """
        Get the optimal area for window layout.
        
        Returns:
            Tuple of (x, y, width, height) for optimal layout area
        """
        if not self.displays:
            return (0, 0, 1920, 1080)  # Default fallback
        
        # For now, use the primary display
        # In a real implementation, you'd calculate the best area across displays
        primary = self.get_primary_display()
        if primary:
            return (0, 0, primary.resolution[0], primary.resolution[1])
        
        return (0, 0, 1920, 1080)
