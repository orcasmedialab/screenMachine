#!/usr/bin/env python3
"""
Wake-on-LAN GUI Utility for Screen Machine
This script provides a simple GUI interface to wake up a remote mini PC.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import sys
from wake_on_lan import WakeOnLAN


class WakeOnLANGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Machine - Wake-on-LAN")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Initialize WakeOnLAN
        self.wol = WakeOnLAN()
        
        # Configuration file
        self.config_file = "wol_config.json"
        self.load_config()
        
        self.setup_ui()
        
    def load_config(self):
        """Load configuration from file."""
        self.config = {
            "mac_address": "",
            "device_name": "",
            "retries": 3,
            "delay": 1.0
        }
        
        # Try to load from config.py first (if it exists)
        try:
            # Check if config.py exists in the same directory
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.py')
            if os.path.exists(config_path):
                import importlib.util
                spec = importlib.util.spec_from_file_location("config", config_path)
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                
                # Load values from config.py
                if hasattr(config_module, 'UBUNTU_MINI_PC'):
                    ubuntu_config = config_module.UBUNTU_MINI_PC
                    self.config["mac_address"] = ubuntu_config.get("mac_address", "")
                    self.config["device_name"] = ubuntu_config.get("name", "")
                
                if hasattr(config_module, 'WOL_SETTINGS'):
                    wol_settings = config_module.WOL_SETTINGS
                    self.config["retries"] = wol_settings.get("retries", 3)
                    self.config["delay"] = wol_settings.get("delay", 1.0)
                    
                print(f"Loaded configuration from config.py")
                return
        except Exception as e:
            print(f"Could not load config.py: {e}")
        
        # Fall back to JSON config file
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    self.config.update(saved_config)
            except Exception as e:
                print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Screen Machine", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, text="Wake-on-LAN Utility (Windows → Ubuntu)", font=("Arial", 12))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Device name
        ttk.Label(main_frame, text="Device Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.device_name_var = tk.StringVar(value=self.config["device_name"])
        device_name_entry = ttk.Entry(main_frame, textvariable=self.device_name_var, width=30)
        device_name_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Help text for device name
        device_help = ttk.Label(main_frame, text="e.g., Ubuntu Mini PC, TV Computer", 
                               font=("Arial", 8), foreground="gray")
        device_help.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(0, 5))
        
        # MAC address
        ttk.Label(main_frame, text="MAC Address:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.mac_address_var = tk.StringVar(value=self.config["mac_address"])
        mac_address_entry = ttk.Entry(main_frame, textvariable=self.mac_address_var, width=30)
        mac_address_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Help text for MAC address format
        help_text = ttk.Label(main_frame, text="Format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX", 
                             font=("Arial", 8), foreground="gray")
        help_text.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Retries
        ttk.Label(main_frame, text="Retries:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.retries_var = tk.IntVar(value=self.config["retries"])
        retries_spinbox = ttk.Spinbox(main_frame, from_=1, to=10, textvariable=self.retries_var, width=10)
        retries_spinbox.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Delay
        ttk.Label(main_frame, text="Delay (seconds):").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.delay_var = tk.DoubleVar(value=self.config["delay"])
        delay_spinbox = ttk.Spinbox(main_frame, from_=0.5, to=5.0, increment=0.5, 
                                   textvariable=self.delay_var, width=10)
        delay_spinbox.grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Wake button
        self.wake_button = ttk.Button(button_frame, text="Wake Up Device", 
                                     command=self.wake_device, style="Accent.TButton")
        self.wake_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Save config button
        save_button = ttk.Button(button_frame, text="Save Config", command=self.save_current_config)
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to wake up Ubuntu mini PC")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                     font=("Arial", 10), foreground="blue")
        self.status_label.grid(row=9, column=0, columnspan=2, pady=(10, 0))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def save_current_config(self):
        """Save current configuration."""
        self.config["device_name"] = self.device_name_var.get()
        self.config["mac_address"] = self.mac_address_var.get()
        self.config["retries"] = self.retries_var.get()
        self.config["delay"] = self.delay_var.get()
        
        self.save_config()
        messagebox.showinfo("Success", "Configuration saved successfully!")
    
    def wake_device(self):
        """Wake up the device."""
        mac_address = self.mac_address_var.get().strip()
        device_name = self.device_name_var.get().strip()
        
        if not mac_address:
            messagebox.showerror("Error", "Please enter a MAC address")
            return
        
        # Validate MAC address format
        try:
            # Remove separators and check length
            clean_mac = mac_address.replace(':', '').replace('-', '').upper()
            if len(clean_mac) != 12:
                raise ValueError("Invalid MAC address length")
            
            # Try to convert to bytes to validate hex format
            bytes.fromhex(clean_mac)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid MAC address format. Use XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX")
            return
        
        # Disable button and show progress
        self.wake_button.config(state='disabled')
        self.status_var.set("Waking up device...")
        self.progress.start()
        
        # Run the wake operation in a separate thread to avoid blocking the GUI
        self.root.after(100, self._wake_device_async, mac_address, device_name)
    
    def _wake_device_async(self, mac_address, device_name):
        """Wake device asynchronously."""
        try:
            retries = self.retries_var.get()
            delay = self.delay_var.get()
            
            success = self.wol.wake_device(mac_address, retries, delay)
            
            if success:
                device_display = device_name if device_name else mac_address
                self.status_var.set(f"Successfully sent wake signal to {device_display}")
                messagebox.showinfo("Success", f"Wake-on-LAN packet sent successfully to {device_display}")
            else:
                self.status_var.set("Failed to wake up device")
                messagebox.showerror("Error", "Failed to send Wake-on-LAN packet")
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable button and stop progress
            self.wake_button.config(state='normal')
            self.progress.stop()


def main():
    root = tk.Tk()
    app = WakeOnLANGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
