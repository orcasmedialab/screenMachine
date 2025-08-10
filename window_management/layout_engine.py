"""
Layout Engine for calculating optimal window arrangements.
"""

import logging
import math
from typing import Dict, List, Tuple, Optional, Any

from .config import *

logger = logging.getLogger(__name__)


class LayoutEngine:
    """
    Calculates optimal window layouts using various algorithms.
    """
    
    def __init__(self):
        """Initialize the Layout Engine."""
        self.grid_size = WINDOW_MANAGEMENT['grid_size']
        self.window_margin = WINDOW_MANAGEMENT['window_margin']
        
        logger.info("Layout Engine initialized")
    
    def calculate_layout(self, 
                        windows: List[Any], 
                        display_info: Dict[str, Any],
                        algorithm: str = "grid") -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Calculate window layout using the specified algorithm.
        
        Args:
            windows: List of Window objects
            display_info: Display information from DisplayManager
            algorithm: Layout algorithm to use
            
        Returns:
            Dictionary mapping window IDs to (position, size) tuples
        """
        try:
            if algorithm == "grid":
                return self._calculate_grid_layout(windows, display_info)
            elif algorithm == "tile":
                return self._calculate_tile_layout(windows, display_info)
            elif algorithm == "cascade":
                return self._calculate_cascade_layout(windows, display_info)
            elif algorithm == "custom":
                return self._calculate_custom_layout(windows, display_info)
            else:
                logger.warning(f"Unknown layout algorithm: {algorithm}, using grid")
                return self._calculate_grid_layout(windows, display_info)
                
        except Exception as e:
            logger.error(f"Error calculating layout: {e}")
            return {}
    
    def _calculate_grid_layout(self, windows: List[Any], display_info: Dict[str, Any]) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Calculate grid-based layout.
        
        Windows are arranged in a grid pattern with equal spacing.
        """
        try:
            if not windows:
                return {}
            
            # Get display dimensions
            display_width, display_height = display_info.get('total_resolution', (1920, 1080))
            
            # Calculate grid dimensions
            num_windows = len(windows)
            grid_cols = math.ceil(math.sqrt(num_windows))
            grid_rows = math.ceil(num_windows / grid_cols)
            
            # Calculate cell dimensions
            cell_width = (display_width - (grid_cols + 1) * self.window_margin) // grid_cols
            cell_height = (display_height - (grid_rows + 1) * self.window_margin) // grid_rows
            
            # Ensure minimum cell size
            cell_width = max(cell_width, MIN_WINDOW_SIZE[0])
            cell_height = max(cell_height, MIN_WINDOW_SIZE[1])
            
            layout = {}
            
            for i, window in enumerate(windows):
                # Calculate grid position
                row = i // grid_cols
                col = i % grid_cols
                
                # Calculate pixel position
                x = self.window_margin + col * (cell_width + self.window_margin)
                y = self.window_margin + row * (cell_height + self.window_margin)
                
                # Ensure position is within display bounds
                x = max(0, min(x, display_width - cell_width))
                y = max(0, min(y, display_height - cell_height))
                
                layout[window.id] = ((x, y), (cell_width, cell_height))
            
            logger.debug(f"Calculated grid layout for {len(windows)} windows")
            return layout
            
        except Exception as e:
            logger.error(f"Error calculating grid layout: {e}")
            return {}
    
    def _calculate_tile_layout(self, windows: List[Any], display_info: Dict[str, Any]) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Calculate tiled layout.
        
        Windows are arranged in a tiled pattern, filling the available space.
        """
        try:
            if not windows:
                return {}
            
            # Get display dimensions
            display_width, display_height = display_info.get('total_resolution', (1920, 1080))
            
            # Calculate tile dimensions based on number of windows
            num_windows = len(windows)
            
            if num_windows == 1:
                # Single window takes full screen
                layout = {
                    windows[0].id: ((0, 0), (display_width, display_height))
                }
            elif num_windows == 2:
                # Two windows side by side
                half_width = (display_width - self.window_margin) // 2
                layout = {
                    windows[0].id: ((0, 0), (half_width, display_height)),
                    windows[1].id: ((half_width + self.window_margin, 0), (half_width, display_height))
                }
            elif num_windows == 3:
                # Three windows: one on top, two below
                top_height = display_height // 2
                bottom_height = (display_height - top_height - self.window_margin)
                half_width = (display_width - self.window_margin) // 2
                
                layout = {
                    windows[0].id: ((0, 0), (display_width, top_height)),
                    windows[1].id: ((0, top_height + self.window_margin), (half_width, bottom_height)),
                    windows[2].id: ((half_width + self.window_margin, top_height + self.window_margin), (half_width, bottom_height))
                }
            else:
                # More than 3 windows: use grid-like tiling
                layout = self._calculate_grid_layout(windows, display_info)
            
            logger.debug(f"Calculated tile layout for {len(windows)} windows")
            return layout
            
        except Exception as e:
            logger.error(f"Error calculating tile layout: {e}")
            return {}
    
    def _calculate_cascade_layout(self, windows: List[Any], display_info: Dict[str, Any]) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Calculate cascading layout.
        
        Windows are arranged in a cascading pattern with slight offsets.
        """
        try:
            if not windows:
                return {}
            
            # Get display dimensions
            display_width, display_height = display_info.get('total_resolution', (1920, 1080))
            
            # Calculate window dimensions
            window_width = min(800, display_width // 2)
            window_height = min(600, display_height // 2)
            
            # Ensure minimum size
            window_width = max(window_width, MIN_WINDOW_SIZE[0])
            window_height = max(window_height, MIN_WINDOW_SIZE[1])
            
            # Cascade offset
            offset_x = 50
            offset_y = 50
            
            layout = {}
            
            for i, window in enumerate(windows):
                # Calculate cascade position
                x = offset_x * i
                y = offset_y * i
                
                # Ensure position is within display bounds
                x = max(0, min(x, display_width - window_width))
                y = max(0, min(y, display_height - window_height))
                
                layout[window.id] = ((x, y), (window_width, window_height))
            
            logger.debug(f"Calculated cascade layout for {len(windows)} windows")
            return layout
            
        except Exception as e:
            logger.error(f"Error calculating cascade layout: {e}")
            return {}
    
    def _calculate_custom_layout(self, windows: List[Any], display_info: Dict[str, Any]) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Calculate custom layout based on window metadata.
        
        This allows for application-specific positioning.
        """
        try:
            if not windows:
                return {}
            
            # Get display dimensions
            display_width, display_height = display_info.get('total_resolution', (1920, 1080))
            
            layout = {}
            
            for i, window in enumerate(windows):
                # Check for custom positioning in metadata
                custom_position = window.metadata.get('custom_position')
                custom_size = window.metadata.get('custom_size')
                
                if custom_position and custom_size:
                    # Use custom positioning
                    x, y = custom_position
                    width, height = custom_size
                else:
                    # Use default positioning
                    x = 100 + (i * 50)
                    y = 100 + (i * 50)
                    width = 800
                    height = 600
                
                # Ensure position and size are within bounds
                x = max(0, min(x, display_width - width))
                y = max(0, min(y, display_height - height))
                width = max(MIN_WINDOW_SIZE[0], min(width, display_width - x))
                height = max(MIN_WINDOW_SIZE[1], min(height, display_height - y))
                
                layout[window.id] = ((x, y), (width, height))
            
            logger.debug(f"Calculated custom layout for {len(windows)} windows")
            return layout
            
        except Exception as e:
            logger.error(f"Error calculating custom layout: {e}")
            return {}
    
    def optimize_layout(self, 
                       windows: List[Any], 
                       display_info: Dict[str, Any],
                       constraints: Optional[Dict[str, Any]] = None) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Optimize layout based on constraints and preferences.
        
        Args:
            windows: List of Window objects
            display_info: Display information
            constraints: Layout constraints (e.g., minimum spacing, preferred positions)
            
        Returns:
            Optimized layout
        """
        try:
            # Start with grid layout
            layout = self._calculate_grid_layout(windows, display_info)
            
            if constraints:
                # Apply constraints
                layout = self._apply_constraints(layout, constraints, display_info)
            
            # Snap to grid if enabled
            if WINDOW_MANAGEMENT['snap_to_grid']:
                layout = self._snap_to_grid(layout)
            
            logger.debug("Layout optimization completed")
            return layout
            
        except Exception as e:
            logger.error(f"Error optimizing layout: {e}")
            return {}
    
    def _apply_constraints(self, 
                          layout: Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]],
                          constraints: Dict[str, Any],
                          display_info: Dict[str, Any]) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Apply layout constraints."""
        try:
            # Apply minimum spacing constraint
            min_spacing = constraints.get('min_spacing', self.window_margin)
            
            # Apply preferred positions
            preferred_positions = constraints.get('preferred_positions', {})
            
            for window_id, (position, size) in layout.items():
                if window_id in preferred_positions:
                    preferred_pos, preferred_size = preferred_positions[window_id]
                    
                    # Use preferred position if it's valid
                    if self._is_valid_position(preferred_pos, preferred_size, display_info):
                        layout[window_id] = (preferred_pos, preferred_size)
            
            return layout
            
        except Exception as e:
            logger.error(f"Error applying constraints: {e}")
            return layout
    
    def _snap_to_grid(self, layout: Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]) -> Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Snap window positions to grid."""
        try:
            snapped_layout = {}
            
            for window_id, (position, size) in layout.items():
                x, y = position
                
                # Snap to grid
                snapped_x = round(x / self.grid_size) * self.grid_size
                snapped_y = round(y / self.grid_size) * self.grid_size
                
                snapped_layout[window_id] = ((snapped_x, snapped_y), size)
            
            return snapped_layout
            
        except Exception as e:
            logger.error(f"Error snapping to grid: {e}")
            return layout
    
    def _is_valid_position(self, position: Tuple[int, int], size: Tuple[int, int], display_info: Dict[str, Any]) -> bool:
        """Check if a position is valid within the display bounds."""
        try:
            x, y = position
            width, height = size
            display_width, display_height = display_info.get('total_resolution', (1920, 1080))
            
            # Check bounds
            if x < 0 or y < 0:
                return False
            if x + width > display_width:
                return False
            if y + height > display_height:
                return False
            
            # Check minimum size
            if width < MIN_WINDOW_SIZE[0] or height < MIN_WINDOW_SIZE[1]:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating position: {e}")
            return False
    
    def get_layout_statistics(self, layout: Dict[int, Tuple[Tuple[int, int], Tuple[int, int]]]) -> Dict[str, Any]:
        """Get statistics about the current layout."""
        try:
            if not layout:
                return {}
            
            # Calculate coverage area
            total_area = 0
            min_x, min_y = float('inf'), float('inf')
            max_x, max_y = 0, 0
            
            for (position, size) in layout.values():
                x, y = position
                width, height = size
                
                total_area += width * height
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x + width)
                max_y = max(max_y, y + height)
            
            # Calculate overlap
            overlap_count = 0
            window_positions = list(layout.values())
            
            for i in range(len(window_positions)):
                for j in range(i + 1, len(window_positions)):
                    if self._windows_overlap(window_positions[i], window_positions[j]):
                        overlap_count += 1
            
            return {
                'total_windows': len(layout),
                'total_area': total_area,
                'bounding_box': (min_x, min_y, max_x - min_x, max_y - min_y),
                'overlap_count': overlap_count,
                'average_window_size': total_area / len(layout) if layout else 0
            }
            
        except Exception as e:
            logger.error(f"Error calculating layout statistics: {e}")
            return {}
    
    def _windows_overlap(self, window1: Tuple[Tuple[int, int], Tuple[int, int]], 
                         window2: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
        """Check if two windows overlap."""
        try:
            (x1, y1), (w1, h1) = window1
            (x2, y2), (w2, h2) = window2
            
            # Check for overlap
            return not (x1 + w1 <= x2 or x2 + w2 <= x1 or y1 + h1 <= y2 or y2 + h2 <= y1)
            
        except Exception as e:
            logger.error(f"Error checking window overlap: {e}")
            return False
