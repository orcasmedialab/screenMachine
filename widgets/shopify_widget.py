"""
Shopify Orders Widget for Screen Machine
Displays Shopify order information (initially mock data)
Designed for easy Shopify API integration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from .base_widget import BaseWidget


class ShopifyWidget(BaseWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="🛍️ Shopify Orders", **kwargs)
        
    def init_content(self):
        """Initialize Shopify orders content"""
        # Mock Shopify order data (replace with Shopify API later)
        self.mock_orders = [
            {
                'order_id': '#1001',
                'customer': 'John Smith',
                'amount': '$89.99',
                'status': 'Fulfilled',
                'date': '2025-01-18',
                'items': 3
            },
            {
                'order_id': '#1002',
                'customer': 'Sarah Johnson',
                'amount': '$156.50',
                'status': 'Processing',
                'date': '2025-01-17',
                'items': 5
            },
            {
                'order_id': '#1003',
                'customer': 'Mike Davis',
                'amount': '$45.00',
                'status': 'Shipped',
                'date': '2025-01-16',
                'items': 2
            },
            {
                'order_id': '#1004',
                'customer': 'Lisa Wilson',
                'amount': '$234.75',
                'status': 'Pending',
                'date': '2025-01-15',
                'items': 7
            },
            {
                'order_id': '#1005',
                'customer': 'Tom Brown',
                'amount': '$67.25',
                'status': 'Fulfilled',
                'date': '2025-01-14',
                'items': 1
            }
        ]
        
        # Create orders display
        self.create_orders_display()
        
        # Create summary stats
        self.create_summary_stats()
        
    def create_orders_display(self):
        """Create the orders list display"""
        # Header
        orders_header = tk.Label(
            self.content_frame,
            text="Recent Orders:",
            bg='#34495e',
            fg='white',
            font=('Arial', 11, 'bold'),
            anchor='w'
        )
        orders_header.pack(fill='x', pady=(0, 10))
        
        # Orders frame
        self.orders_frame = tk.Frame(self.content_frame, bg='#34495e')
        self.orders_frame.pack(fill='both', expand=True)
        
        # Create order entries
        self.create_order_entries()
        
    def create_order_entries(self):
        """Create individual order entry widgets"""
        for i, order in enumerate(self.mock_orders):
            # Order container
            order_frame = tk.Frame(self.orders_frame, bg='#2c3e50', relief='flat', borderwidth=1)
            order_frame.pack(fill='x', pady=2, padx=5)
            
            # Order header
            header_frame = tk.Frame(order_frame, bg='#2c3e50')
            header_frame.pack(fill='x', padx=10, pady=5)
            
            # Order ID
            order_id_label = tk.Label(
                header_frame,
                text=order['order_id'],
                bg='#2c3e50',
                fg='#3498db',
                font=('Arial', 10, 'bold')
            )
            order_id_label.pack(side='left')
            
            # Status badge
            status_color = self.get_status_color(order['status'])
            status_label = tk.Label(
                header_frame,
                text=order['status'],
                bg=status_color,
                fg='white',
                font=('Arial', 8, 'bold'),
                padx=8,
                pady=2
            )
            status_label.pack(side='right')
            
            # Order details
            details_frame = tk.Frame(order_frame, bg='#2c3e50')
            details_frame.pack(fill='x', padx=10, pady=(0, 5))
            
            # Customer name
            customer_label = tk.Label(
                details_frame,
                text=order['customer'],
                bg='#2c3e50',
                fg='white',
                font=('Arial', 11, 'bold')
            )
            customer_label.pack(side='left')
            
            # Amount
            amount_label = tk.Label(
                details_frame,
                text=order['amount'],
                bg='#2c3e50',
                fg='#27ae60',
                font=('Arial', 11, 'bold')
            )
            amount_label.pack(side='right')
            
            # Additional info
            info_frame = tk.Frame(order_frame, bg='#2c3e50')
            info_frame.pack(fill='x', padx=10, pady=(0, 5))
            
            # Date
            date_label = tk.Label(
                info_frame,
                text=f"Date: {order['date']}",
                bg='#2c3e50',
                fg='#95a5a6',
                font=('Arial', 9)
            )
            date_label.pack(side='left')
            
            # Items count
            items_label = tk.Label(
                info_frame,
                text=f"Items: {order['items']}",
                bg='#2c3e50',
                fg='#95a5a6',
                font=('Arial', 9)
            )
            items_label.pack(side='right')
            
            # Separator
            if i < len(self.mock_orders) - 1:
                separator = tk.Frame(order_frame, height=1, bg='#34495e')
                separator.pack(fill='x', pady=5)
                
    def get_status_color(self, status):
        """Get color for order status"""
        status_colors = {
            'Pending': '#f39c12',
            'Processing': '#3498db',
            'Shipped': '#9b59b6',
            'Fulfilled': '#27ae60',
            'Cancelled': '#e74c3c'
        }
        return status_colors.get(status, '#95a5a6')
        
    def create_summary_stats(self):
        """Create summary statistics display"""
        # Stats header
        stats_header = tk.Label(
            self.content_frame,
            text="Store Summary:",
            bg='#34495e',
            fg='white',
            font=('Arial', 11, 'bold'),
            anchor='w'
        )
        stats_header.pack(fill='x', pady=(15, 10))
        
        # Stats frame
        stats_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        stats_frame.pack(fill='x', padx=5, pady=(0, 10))
        
        # Calculate mock stats
        total_orders = len(self.mock_orders)
        total_revenue = sum(float(order['amount'].replace('$', '')) for order in self.mock_orders)
        pending_orders = len([order for order in self.mock_orders if order['status'] == 'Pending'])
        fulfilled_orders = len([order for order in self.mock_orders if order['status'] == 'Fulfilled'])
        
        stats_data = [
            ("Total Orders", str(total_orders)),
            ("Total Revenue", f"${total_revenue:.2f}"),
            ("Pending", str(pending_orders)),
            ("Fulfilled", str(fulfilled_orders))
        ]
        
        # Create stats grid
        for i, (stat, value) in enumerate(stats_data):
            # Stat label
            stat_label = tk.Label(
                stats_frame,
                text=stat,
                bg='#2c3e50',
                fg='#95a5a6',
                font=('Arial', 9),
                anchor='w'
            )
            stat_label.grid(row=i, column=0, sticky='w', padx=10, pady=3)
            
            # Value label
            value_label = tk.Label(
                stats_frame,
                text=value,
                bg='#2c3e50',
                fg='white',
                font=('Arial', 9, 'bold'),
                anchor='w'
            )
            value_label.grid(row=i, column=1, sticky='w', padx=(20, 10), pady=3)
            
        # Configure grid weights
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
        
    def refresh(self):
        """Refresh order data (for future API integration)"""
        # In the future, this will fetch data from Shopify API
        # Clear and recreate order entries
        for widget in self.orders_frame.winfo_children():
            widget.destroy()
        self.create_order_entries()
        
        # Update summary stats
        for widget in self.content_frame.winfo_children():
            if hasattr(widget, 'winfo_name') and 'stats_frame' in str(widget):
                widget.destroy()
        self.create_summary_stats()
