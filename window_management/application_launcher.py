"""
Application Launcher for managing application processes and windows.
"""

import logging
import subprocess
import psutil
import time
import os
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from .config import *

logger = logging.getLogger(__name__)


@dataclass
class ProcessInfo:
    """Process information container."""
    pid: int
    name: str
    command: str
    args: List[str]
    status: str
    created_at: float
    metadata: Dict[str, Any]


class ApplicationLauncher:
    """
    Manages application launching and process management for the Screen Machine system.
    """
    
    def __init__(self):
        """Initialize the Application Launcher."""
        self.processes: Dict[int, ProcessInfo] = {}
        self.process_counter = 0
        
        logger.info("Application Launcher initialized")
    
    def launch_browser(self, browser: str, url: str, args: Optional[List[str]] = None) -> subprocess.Popen:
        """
        Launch a browser with the specified URL.
        
        Args:
            browser: Browser to launch (firefox, chromium, chrome)
            url: URL to open
            args: Additional command line arguments
            
        Returns:
            Popen object representing the launched process
        """
        try:
            # Validate browser
            if browser not in APPLICATION_PATHS:
                raise ValueError(f"Unsupported browser: {browser}")
            
            # Get browser path
            browser_path = APPLICATION_PATHS[browser]
            if not os.path.exists(browser_path):
                # Try to find browser in PATH
                browser_path = browser
            
            # Prepare command
            cmd = [browser_path]
            
            # Add browser-specific options
            if browser in BROWSER_OPTIONS:
                cmd.extend(BROWSER_OPTIONS[browser])
            
            # Add custom arguments
            if args:
                cmd.extend(args)
            
            # Add URL
            cmd.append(url)
            
            # Launch process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            
            # Store process information
            process_info = ProcessInfo(
                pid=process.pid,
                name=browser,
                command=browser_path,
                args=cmd[1:],
                status="running",
                created_at=time.time(),
                metadata={'url': url, 'type': 'browser'}
            )
            
            self.processes[process.pid] = process_info
            self.process_counter += 1
            
            logger.info(f"Launched {browser} with URL: {url} (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"Failed to launch browser {browser}: {e}")
            raise
    
    def launch_application(self, command: str, args: Optional[List[str]] = None) -> subprocess.Popen:
        """
        Launch a local application.
        
        Args:
            command: Application command to run
            args: Additional command line arguments
            
        Returns:
            Popen object representing the launched process
        """
        try:
            # Prepare command
            cmd = [command]
            if args:
                cmd.extend(args)
            
            # Launch process
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            
            # Store process information
            process_info = ProcessInfo(
                pid=process.pid,
                name=command,
                command=command,
                args=args or [],
                status="running",
                created_at=time.time(),
                metadata={'type': 'application'}
            )
            
            self.processes[process.pid] = process_info
            self.process_counter += 1
            
            logger.info(f"Launched application: {command} (PID: {process.pid})")
            return process
            
        except Exception as e:
            logger.error(f"Failed to launch application {command}: {e}")
            raise
    
    def launch_web_application(self, url: str, title: str = None, browser: str = None) -> subprocess.Popen:
        """
        Launch a web application in a browser.
        
        Args:
            url: URL to open
            title: Custom title for the window
            browser: Specific browser to use
            
        Returns:
            Popen object representing the launched process
        """
        browser = browser or DEFAULT_BROWSER
        
        # Add title-specific arguments if supported
        args = []
        if title and browser == "firefox":
            args.extend(["--name", title])
        elif title and browser in ["chromium", "google-chrome"]:
            args.extend(["--app-name", title])
        
        return self.launch_browser(browser, url, args)
    
    def terminate_process(self, pid: int) -> bool:
        """
        Terminate a specific process.
        
        Args:
            pid: Process ID to terminate
            
        Returns:
            True if process was terminated successfully
        """
        try:
            if pid not in self.processes:
                logger.warning(f"Process {pid} not found in tracking")
                return False
            
            process_info = self.processes[pid]
            
            # Try graceful termination first
            try:
                process = psutil.Process(pid)
                process.terminate()
                
                # Wait for graceful termination
                try:
                    process.wait(timeout=5)
                    logger.info(f"Process {pid} terminated gracefully")
                except psutil.TimeoutExpired:
                    # Force kill if graceful termination fails
                    process.kill()
                    logger.info(f"Process {pid} force killed")
                
            except psutil.NoSuchProcess:
                logger.info(f"Process {pid} already terminated")
            
            # Remove from tracking
            del self.processes[pid]
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to terminate process {pid}: {e}")
            return False
    
    def get_process_info(self, pid: int) -> Optional[ProcessInfo]:
        """Get information about a specific process."""
        return self.processes.get(pid)
    
    def list_processes(self) -> List[ProcessInfo]:
        """Get a list of all tracked processes."""
        return list(self.processes.values())
    
    def get_process_count(self) -> int:
        """Get the total number of tracked processes."""
        return len(self.processes)
    
    def is_process_running(self, pid: int) -> bool:
        """Check if a process is still running."""
        try:
            if pid not in self.processes:
                return False
            
            process = psutil.Process(pid)
            return process.is_running()
            
        except psutil.NoSuchProcess:
            return False
        except Exception as e:
            logger.error(f"Error checking process {pid}: {e}")
            return False
    
    def refresh_process_status(self):
        """Refresh the status of all tracked processes."""
        try:
            terminated_pids = []
            
            for pid, process_info in self.processes.items():
                if not self.is_process_running(pid):
                    process_info.status = "terminated"
                    terminated_pids.append(pid)
                else:
                    process_info.status = "running"
            
            # Remove terminated processes
            for pid in terminated_pids:
                del self.processes[pid]
            
            if terminated_pids:
                logger.info(f"Removed {len(terminated_pids)} terminated processes")
                
        except Exception as e:
            logger.error(f"Error refreshing process status: {e}")
    
    def get_process_by_name(self, name: str) -> List[ProcessInfo]:
        """Get all processes with a specific name."""
        return [p for p in self.processes.values() if p.name == name]
    
    def get_browser_processes(self) -> List[ProcessInfo]:
        """Get all browser processes."""
        return [p for p in self.processes.values() if p.metadata.get('type') == 'browser']
    
    def get_application_processes(self) -> List[ProcessInfo]:
        """Get all application processes."""
        return [p for p in self.processes.values() if p.metadata.get('type') == 'application']
    
    def cleanup_terminated_processes(self):
        """Remove all terminated processes from tracking."""
        try:
            terminated_pids = [
                pid for pid, process_info in self.processes.items()
                if process_info.status == "terminated"
            ]
            
            for pid in terminated_pids:
                del self.processes[pid]
            
            if terminated_pids:
                logger.info(f"Cleaned up {len(terminated_pids)} terminated processes")
                
        except Exception as e:
            logger.error(f"Error cleaning up terminated processes: {e}")
    
    def get_system_processes(self) -> List[Dict[str, Any]]:
        """Get information about all system processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'create_time']):
                try:
                    processes.append({
                        'pid': proc.info['pid'],
                        'name': proc.info['name'],
                        'status': proc.info['status'],
                        'created_at': proc.info['create_time']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            return processes
            
        except Exception as e:
            logger.error(f"Error getting system processes: {e}")
            return []
    
    def cleanup(self):
        """Clean up resources and terminate all tracked processes."""
        try:
            for pid in list(self.processes.keys()):
                self.terminate_process(pid)
            
            logger.info("Application Launcher cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.cleanup()
