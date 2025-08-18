"""
Yankees Game Widget for Screen Machine
Displays Yankees game information (initially mock data)
Designed for easy sports API integration
"""

import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from .base_widget import BaseWidget


class YankeesWidget(BaseWidget):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, title="⚾ Yankees Games", **kwargs)
        
    def init_content(self):
        """Initialize Yankees game content"""
        # Mock Yankees game data (replace with sports API later)
        self.mock_games = [
            {
                'date': '2025-01-18',
                'opponent': 'Boston Red Sox',
                'time': '7:00 PM',
                'venue': 'Yankee Stadium',
                'status': 'Upcoming',
                'score': None
            },
            {
                'date': '2025-01-20',
                'opponent': 'Toronto Blue Jays',
                'time': '1:00 PM',
                'venue': 'Rogers Centre',
                'status': 'Upcoming',
                'score': None
            },
            {
                'date': '2025-01-15',
                'opponent': 'Baltimore Orioles',
                'time': '7:00 PM',
                'venue': 'Yankee Stadium',
                'status': 'Final',
                'score': 'Yankees 6 - Orioles 3'
            },
            {
                'date': '2025-01-12',
                'opponent': 'Tampa Bay Rays',
                'time': '7:00 PM',
                'venue': 'Tropicana Field',
                'status': 'Final',
                'score': 'Yankees 4 - Rays 7'
            }
        ]
        
        # Create game display
        self.create_games_display()
        
        # Create team stats
        self.create_team_stats()
        
    def create_games_display(self):
        """Create the games list display"""
        # Header
        games_header = tk.Label(
            self.content_frame,
            text="Recent & Upcoming Games:",
            bg='#34495e',
            fg='white',
            font=('Arial', 11, 'bold'),
            anchor='w'
        )
        games_header.pack(fill='x', pady=(0, 10))
        
        # Games frame
        self.games_frame = tk.Frame(self.content_frame, bg='#34495e')
        self.games_frame.pack(fill='both', expand=True)
        
        # Create game entries
        self.create_game_entries()
        
    def create_game_entries(self):
        """Create individual game entry widgets"""
        for i, game in enumerate(self.mock_games):
            # Game container
            game_frame = tk.Frame(self.games_frame, bg='#2c3e50', relief='flat', borderwidth=1)
            game_frame.pack(fill='x', pady=2, padx=5)
            
            # Date and status
            info_frame = tk.Frame(game_frame, bg='#2c3e50')
            info_frame.pack(fill='x', padx=10, pady=5)
            
            # Date
            date_label = tk.Label(
                info_frame,
                text=game['date'],
                bg='#2c3e50',
                fg='#95a5a6',
                font=('Arial', 9)
            )
            date_label.pack(side='left')
            
            # Status badge
            status_color = '#e74c3c' if game['status'] == 'Final' else '#27ae60'
            status_label = tk.Label(
                info_frame,
                text=game['status'],
                bg=status_color,
                fg='white',
                font=('Arial', 8, 'bold'),
                padx=8,
                pady=2
            )
            status_label.pack(side='right')
            
            # Game details
            details_frame = tk.Frame(game_frame, bg='#2c3e50')
            details_frame.pack(fill='x', padx=10, pady=(0, 5))
            
            # Opponent
            opponent_label = tk.Label(
                details_frame,
                text=f"vs {game['opponent']}",
                bg='#2c3e50',
                fg='white',
                font=('Arial', 12, 'bold')
            )
            opponent_label.pack(side='left')
            
            # Time
            time_label = tk.Label(
                details_frame,
                text=game['time'],
                bg='#2c3e50',
                fg='#3498db',
                font=('Arial', 10)
            )
            time_label.pack(side='right')
            
            # Venue
            venue_label = tk.Label(
                game_frame,
                text=game['venue'],
                bg='#2c3e50',
                fg='#95a5a6',
                font=('Arial', 9),
                anchor='w'
            )
            venue_label.pack(fill='x', padx=10, pady=(0, 5))
            
            # Score (if game is final)
            if game['score']:
                score_label = tk.Label(
                    game_frame,
                    text=game['score'],
                    bg='#2c3e50',
                    fg='#f39c12',
                    font=('Arial', 11, 'bold'),
                    anchor='w'
                )
                score_label.pack(fill='x', padx=10, pady=(0, 5))
            
            # Separator
            if i < len(self.mock_games) - 1:
                separator = tk.Frame(game_frame, height=1, bg='#34495e')
                separator.pack(fill='x', pady=5)
                
    def create_team_stats(self):
        """Create team statistics display"""
        # Stats header
        stats_header = tk.Label(
            self.content_frame,
            text="Team Stats:",
            bg='#34495e',
            fg='white',
            font=('Arial', 11, 'bold'),
            anchor='w'
        )
        stats_header.pack(fill='x', pady=(15, 10))
        
        # Stats frame
        stats_frame = tk.Frame(self.content_frame, bg='#2c3e50')
        stats_frame.pack(fill='x', padx=5, pady=(0, 10))
        
        # Mock stats (replace with real API data)
        stats_data = [
            ("Record", "87-75"),
            ("Games Back", "12.5"),
            ("Last 10", "6-4"),
            ("Streak", "W2")
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
        """Refresh game data (for future API integration)"""
        # In the future, this will fetch data from sports API
        # Clear and recreate game entries
        for widget in self.games_frame.winfo_children():
            widget.destroy()
        self.create_game_entries()
