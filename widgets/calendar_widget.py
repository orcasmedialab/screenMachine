"""
Calendar Widget for Screen Machine
Displays monthly calendar with events (initially mock data)
Designed for easy Google Calendar API integration
"""

import tkinter as tk
from tkinter import ttk
import calendar
import datetime
from .base_widget import BaseWidget


class CalendarWidget(BaseWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="📅 Calendar", **kwargs)
        
    def init_content(self):
        """Initialize calendar content"""
        # Get current date
        self.current_date = datetime.datetime.now()
        self.current_year = self.current_date.year
        self.current_month = self.current_date.month
        
        # Mock events data (replace with Google Calendar API later)
        self.mock_events = {
            (2025, 1, 15): "Team Meeting - 10:00 AM",
            (2025, 1, 18): "Yankees Game - 7:00 PM",
            (2025, 1, 22): "Shopify Review - 2:00 PM",
            (2025, 1, 25): "Amazon Inventory Check - 9:00 AM",
            (2025, 1, 28): "System Maintenance - 11:00 PM",
            (2025, 1, 30): "Monthly Report Due",
        }
        
        # Create calendar display
        self.create_calendar_display()
        
        # Create events list
        self.create_events_list()
        
    def create_calendar_display(self):
        """Create the monthly calendar grid"""
        # Month navigation
        nav_frame = tk.Frame(self.content_frame, bg='#34495e')
        nav_frame.pack(fill='x', pady=(0, 10))
        
        # Previous month button
        self.prev_btn = tk.Button(
            nav_frame,
            text="◀",
            command=self.previous_month,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        self.prev_btn.pack(side='left', padx=5)
        
        # Month/Year label
        self.month_label = tk.Label(
            nav_frame,
            text="",
            bg='#34495e',
            fg='white',
            font=('Arial', 14, 'bold')
        )
        self.month_label.pack(side='left', expand=True)
        
        # Next month button
        self.next_btn = tk.Button(
            nav_frame,
            text="▶",
            command=self.next_month,
            bg='#3498db',
            fg='white',
            font=('Arial', 10, 'bold'),
            relief='flat'
        )
        self.next_btn.pack(side='right', padx=5)
        
        # Calendar grid
        self.calendar_frame = tk.Frame(self.content_frame, bg='#34495e')
        self.calendar_frame.pack(fill='both', expand=True)
        
        # Day headers
        days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        for i, day in enumerate(days):
            header = tk.Label(
                self.calendar_frame,
                text=day,
                bg='#2c3e50',
                fg='white',
                font=('Arial', 10, 'bold'),
                width=8,
                height=2
            )
            header.grid(row=0, column=i, sticky='nsew', padx=1, pady=1)
        
        # Configure grid weights
        for i in range(7):
            self.calendar_frame.grid_columnconfigure(i, weight=1)
        
        # Update calendar display
        self.update_calendar_display()
        
    def update_calendar_display(self):
        """Update the calendar display for current month/year"""
        # Update month label
        month_name = calendar.month_name[self.current_month]
        self.month_label.config(text=f"{month_name} {self.current_year}")
        
        # Clear existing calendar days
        for widget in self.calendar_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.grid_info()['row'] > 0:
                widget.destroy()
        
        # Get calendar data
        cal = calendar.monthcalendar(self.current_year, self.current_month)
        
        # Create day labels
        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day != 0:
                    # Check if this day has events
                    has_events = (self.current_year, self.current_month, day) in self.mock_events
                    
                    # Create day label
                    day_label = tk.Label(
                        self.calendar_frame,
                        text=str(day),
                        bg='#e74c3c' if has_events else '#34495e',
                        fg='white',
                        font=('Arial', 10, 'bold'),
                        width=8,
                        height=2,
                        relief='flat'
                    )
                    day_label.grid(row=week_num + 1, column=day_num, sticky='nsew', padx=1, pady=1)
                    
                    # Highlight today
                    if (day == self.current_date.day and 
                        self.current_month == self.current_date.month and 
                        self.current_year == self.current_date.year):
                        day_label.config(bg='#f39c12')
                        
                    # Bind click event to show events
                    day_label.bind('<Button-1>', lambda e, d=day: self.show_day_events(d))
        
        # Configure row weights
        for i in range(1, len(cal) + 1):
            self.calendar_frame.grid_rowconfigure(i, weight=1)
            
    def create_events_list(self):
        """Create the events list below calendar"""
        # Events header
        events_header = tk.Label(
            self.content_frame,
            text="Today's Events:",
            bg='#34495e',
            fg='white',
            font=('Arial', 11, 'bold'),
            anchor='w'
        )
        events_header.pack(fill='x', pady=(10, 5))
        
        # Events list
        self.events_listbox = tk.Listbox(
            self.content_frame,
            bg='#2c3e50',
            fg='white',
            font=('Arial', 9),
            height=4,
            relief='flat',
            selectmode='none'
        )
        self.events_listbox.pack(fill='x', pady=(0, 10))
        
        # Update events list
        self.update_events_list()
        
    def update_events_list(self):
        """Update the events list for today"""
        self.events_listbox.delete(0, tk.END)
        
        today = (self.current_date.year, self.current_date.month, self.current_date.day)
        if today in self.mock_events:
            self.events_listbox.insert(tk.END, self.mock_events[today])
        else:
            self.events_listbox.insert(tk.END, "No events scheduled")
            
    def show_day_events(self, day):
        """Show events for a specific day"""
        events = self.mock_events.get((self.current_year, self.current_month, day), [])
        if events:
            messagebox.showinfo(f"Events for {day}", events)
        else:
            messagebox.showinfo(f"Events for {day}", "No events scheduled")
            
    def previous_month(self):
        """Go to previous month"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar_display()
        
    def next_month(self):
        """Go to next month"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar_display()
        
    def refresh(self):
        """Refresh calendar data (for future API integration)"""
        # In the future, this will fetch data from Google Calendar API
        self.update_calendar_display()
        self.update_events_list()
