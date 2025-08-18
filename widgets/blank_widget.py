"""
Blank Widget for Screen Machine
Placeholder widget for future functionality
"""

import tkinter as tk
from tkinter import ttk
from .base_widget import BaseWidget


class BlankWidget(BaseWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="🔲 Blank Space", **kwargs)
        
    def init_content(self):
        """Initialize blank widget content"""
        # Main content area
        content_area = tk.Frame(self.content_frame, bg='#34495e')
        content_area.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome message
        welcome_label = tk.Label(
            content_area,
            text="Future Widget Space",
            bg='#34495e',
            fg='#95a5a6',
            font=('Arial', 16, 'bold')
        )
        welcome_label.pack(pady=(50, 20))
        
        # Description
        desc_label = tk.Label(
            content_area,
            text="This space is reserved for future functionality.\n\nPossible uses:\n• Weather widget\n• News feed\n• System monitoring\n• Custom integrations\n• Additional business tools",
            bg='#34495e',
            fg='#7f8c8d',
            font=('Arial', 11),
            justify='center'
        )
        desc_label.pack(pady=20)
        
        # Placeholder button (can be removed or customized later)
        placeholder_btn = tk.Button(
            content_area,
            text="Customize This Widget",
            command=self.show_customization_info,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=10
        )
        placeholder_btn.pack(pady=20)
        
        # Status indicator
        status_frame = tk.Frame(content_area, bg='#34495e')
        status_frame.pack(fill='x', pady=(30, 0))
        
        status_label = tk.Label(
            status_frame,
            text="Status: Ready for customization",
            bg='#34495e',
            fg='#27ae60',
            font=('Arial', 9)
        )
        status_label.pack()
        
    def show_customization_info(self):
        """Show information about customizing this widget"""
        info_text = """This widget can be customized for various purposes:

• Weather information display
• News and RSS feeds
• System monitoring and alerts
• Social media feeds
• Stock market data
• Custom business metrics
• Integration with other APIs
• Real-time data streams

To customize, modify the blank_widget.py file
or create a new widget class."""
        
        # Create a simple info dialog
        dialog = tk.Toplevel(self)
        dialog.title("Widget Customization")
        dialog.geometry("500x400")
        dialog.configure(bg='#2c3e50')
        dialog.transient(self)
        dialog.grab_set()
        
        # Center the dialog
        dialog.geometry("+%d+%d" % (self.winfo_rootx() + 50, self.winfo_rooty() + 50))
        
        # Content
        title_label = tk.Label(
            dialog,
            text="Widget Customization Options",
            bg='#2c3e50',
            fg='white',
            font=('Arial', 14, 'bold')
        )
        title_label.pack(pady=20)
        
        text_widget = tk.Text(
            dialog,
            bg='#34495e',
            fg='white',
            font=('Arial', 10),
            wrap='word',
            height=15,
            relief='flat',
            padx=15,
            pady=15
        )
        text_widget.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = tk.Button(
            dialog,
            text="Close",
            command=dialog.destroy,
            bg='#e74c3c',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat',
            padx=20,
            pady=5
        )
        close_btn.pack(pady=(0, 20))
        
    def refresh(self):
        """Refresh widget data (placeholder for future functionality)"""
        # This method can be overridden when the widget is customized
        pass
