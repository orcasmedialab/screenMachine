"""
Base Widget Class for Screen Machine
Provides consistent styling and behavior for all widgets
"""

import tkinter as tk
from tkinter import ttk


class BaseWidget(tk.Frame):
    def __init__(self, parent, title="Widget", **kwargs):
        super().__init__(parent, **kwargs)
        
        # Configure the frame
        self.configure(
            bg='#34495e',
            relief='raised',
            borderwidth=2
        )
        
        # Create title bar
        self.title_bar = tk.Frame(self, bg='#2c3e50', height=40)
        self.title_bar.pack(fill='x', padx=2, pady=2)
        self.title_bar.pack_propagate(False)
        
        # Title label
        self.title_label = tk.Label(
            self.title_bar,
            text=title,
            bg='#2c3e50',
            fg='white',
            font=('Arial', 12, 'bold')
        )
        self.title_label.pack(side='left', padx=10, pady=8)
        
        # Content area
        self.content_frame = tk.Frame(self, bg='#34495e')
        self.content_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Initialize widget content
        self.init_content()
        
    def init_content(self):
        """Override this method in subclasses to add widget-specific content"""
        pass
        
    def refresh(self):
        """Override this method in subclasses to refresh widget data"""
        pass
