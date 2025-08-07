#!/usr/bin/env python3
"""
Wake-on-LAN Utility for Screen Machine
This script sends Wake-on-LAN packets to wake up a remote mini PC.
"""

import socket
import struct
import argparse
import time
import sys
from typing import Optional


class WakeOnLAN:
    def __init__(self):
        self.broadcast_address = '<broadcast>'
        self.port = 9  # Standard WoL port
        
    def create_magic_packet(self, mac_address: str) -> bytes:
        """
        Create a Wake-on-LAN magic packet.
        
        Args:
            mac_address: MAC address in format XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX
            
        Returns:
            Magic packet as bytes
        """
        # Remove any separators and convert to uppercase
        mac_address = mac_address.replace(':', '').replace('-', '').upper()
        
        if len(mac_address) != 12:
            raise ValueError("MAC address must be 12 characters long")
        
        # Create the magic packet
        # 6 bytes of 0xFF followed by 16 repetitions of the MAC address
        magic_packet = b'\xff' * 6 + bytes.fromhex(mac_address) * 16
        
        return magic_packet
    
    def send_magic_packet(self, mac_address: str, broadcast_address: Optional[str] = None) -> bool:
        """
        Send a Wake-on-LAN magic packet to wake up a device.
        
        Args:
            mac_address: MAC address of the target device
            broadcast_address: Broadcast address (optional, defaults to '<broadcast>')
            
        Returns:
            True if packet was sent successfully, False otherwise
        """
        try:
            # Create the magic packet
            magic_packet = self.create_magic_packet(mac_address)
            
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            
            # Send the packet
            target_address = broadcast_address or self.broadcast_address
            sock.sendto(magic_packet, (target_address, self.port))
            sock.close()
            
            return True
            
        except Exception as e:
            print(f"Error sending Wake-on-LAN packet: {e}")
            return False
    
    def wake_device(self, mac_address: str, retries: int = 3, delay: float = 1.0) -> bool:
        """
        Wake up a device with retry logic.
        
        Args:
            mac_address: MAC address of the target device
            retries: Number of retry attempts
            delay: Delay between retries in seconds
            
        Returns:
            True if at least one packet was sent successfully, False otherwise
        """
        print(f"Attempting to wake up device with MAC address: {mac_address}")
        
        success = False
        for attempt in range(1, retries + 1):
            print(f"Attempt {attempt}/{retries}...")
            
            if self.send_magic_packet(mac_address):
                success = True
                print(f"Wake-on-LAN packet sent successfully (attempt {attempt})")
            else:
                print(f"Failed to send Wake-on-LAN packet (attempt {attempt})")
            
            if attempt < retries:
                print(f"Waiting {delay} seconds before next attempt...")
                time.sleep(delay)
        
        if success:
            print("Wake-on-LAN sequence completed successfully!")
        else:
            print("Failed to send Wake-on-LAN packet after all attempts.")
        
        return success


def main():
    parser = argparse.ArgumentParser(
        description="Wake-on-LAN utility for Screen Machine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python wake_on_lan.py 00:11:22:33:44:55
  python wake_on_lan.py 00-11-22-33-44-55 --retries 5
  python wake_on_lan.py 00:11:22:33:44:55 --delay 2.0
        """
    )
    
    parser.add_argument(
        'mac_address',
        help='MAC address of the target device (format: XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)'
    )
    
    parser.add_argument(
        '--retries',
        type=int,
        default=3,
        help='Number of retry attempts (default: 3)'
    )
    
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between retries in seconds (default: 1.0)'
    )
    
    parser.add_argument(
        '--broadcast',
        default='<broadcast>',
        help='Broadcast address (default: <broadcast>)'
    )
    
    args = parser.parse_args()
    
    # Create WakeOnLAN instance
    wol = WakeOnLAN()
    
    # Attempt to wake the device
    success = wol.wake_device(args.mac_address, args.retries, args.delay)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
