#!/usr/bin/env python3
"""
Screen Machine - Full Screen Application Manager
A comprehensive screen management system with multiple widget windows
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from pathlib import Path

# Import our custom widgets
from widgets.calendar_widget import CalendarWidget
from widgets.yankees_widget import YankeesWidget
from widgets.shopify_widget import ShopifyWidget
from widgets.blank_widget import BlankWidget


class ScreenMachine:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Machine")
        self.root.configure(bg='#2c3e50')
        
        # Make it full screen
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-zoomed', True)  # For Windows
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        
        # Initialize widgets
        self.init_widgets()
        
        # Bind escape key to exit full screen
        self.root.bind('<Escape>', self.toggle_fullscreen)
        self.root.bind('<F11>', self.toggle_fullscreen)
        
        # Status bar
        self.create_status_bar()
        
    def init_widgets(self):
        """Initialize all widget windows"""
        # Calendar widget (left side, smaller)
        self.calendar_widget = CalendarWidget(self.root)
        self.calendar_widget.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=5, pady=5)
        
        # Right side widgets (larger area)
        # Yankees game widget (top right)
        self.yankees_widget = YankeesWidget(self.root)
        self.yankees_widget.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Shopify orders widget (bottom right)
        self.shopify_widget = ShopifyWidget(self.root)
        self.shopify_widget.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        
        # Blank widget (can be added later or used for other purposes)
        # self.blank_widget = BlankWidget(self.root)
        # self.blank_widget.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        
    def create_status_bar(self):
        """Create a status bar at the bottom"""
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.grid(row=2, column=0, columnspan=2, sticky='ew')
        status_frame.grid_propagate(False)
        
        # Current time
        self.time_label = tk.Label(status_frame, text="", bg='#34495e', fg='white', font=('Arial', 10))
        self.time_label.pack(side='left', padx=10)
        
        # Status message
        self.status_label = tk.Label(status_frame, text="Screen Machine Ready", bg='#34495e', fg='white', font=('Arial', 10))
        self.status_label.pack(side='right', padx=10)
        
        # Update time
        self.update_time()
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode"""
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


if __name__ == "__main__":
    app = ScreenMachine()
    app.run()
