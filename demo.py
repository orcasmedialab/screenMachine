#!/usr/bin/env python3
"""
Screen Machine Demo
A preview version that doesn't go full-screen for testing purposes
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


class ScreenMachineDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Screen Machine - Demo Mode")
        self.root.configure(bg='#2c3e50')
        
        # Set a reasonable size for demo (not full-screen)
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)
        
        # Initialize widgets
        self.init_widgets()
        
        # Status bar
        self.create_status_bar()
        
        # Demo instructions
        self.create_demo_instructions()
        
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
        
    def create_status_bar(self):
        """Create a status bar at the bottom"""
        status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        status_frame.grid(row=2, column=0, columnspan=2, sticky='ew')
        status_frame.grid_propagate(False)
        
        # Current time
        self.time_label = tk.Label(status_frame, text="", bg='#34495e', fg='white', font=('Arial', 10))
        self.time_label.pack(side='left', padx=10)
        
        # Status message
        self.status_label = tk.Label(status_frame, text="Demo Mode - Press F11 for Full Screen", bg='#34495e', fg='white', font=('Arial', 10))
        self.status_label.pack(side='right', padx=10)
        
        # Update time
        self.update_time()
        
    def create_demo_instructions(self):
        """Create demo instructions at the top"""
        instructions_frame = tk.Frame(self.root, bg='#e74c3c', height=40)
        instructions_frame.grid(row=3, column=0, columnspan=2, sticky='ew')
        instructions_frame.grid_propagate(False)
        
        instructions_text = "DEMO MODE: This is a preview version. Use F11 for full-screen or run screen_machine.py for the full experience."
        instructions_label = tk.Label(
            instructions_frame, 
            text=instructions_text, 
            bg='#e74c3c', 
            fg='white', 
            font=('Arial', 10, 'bold')
        )
        instructions_label.pack(expand=True, pady=10)
        
    def update_time(self):
        """Update the time display"""
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()


if __name__ == "__main__":
    print("Starting Screen Machine Demo...")
    print("This is a preview version that doesn't go full-screen.")
    print("Press F11 to toggle full-screen mode.")
    print("Run 'python3 screen_machine.py' for the full experience.")
    print()
    
    app = ScreenMachineDemo()
    app.run()
