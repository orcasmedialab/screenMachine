#!/bin/bash

# Screen Machine Production Startup Script for Ubuntu
# This script is designed for production use and auto-start services

set -e  # Exit on any error

# Configuration
APP_NAME="Screen Machine"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$APP_DIR/screen_machine.log"
PID_FILE="$APP_DIR/screen_machine.pid"
PYTHON_CMD="python3"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[$(date '+%m-%d %H:%M:%S')] INFO:${NC} $1" | tee -a "$LOG_FILE"
}

# Check if already running
check_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # Running
        else
            # Remove stale PID file
            rm -f "$PID_FILE"
        fi
    fi
    return 1  # Not running
}

# Start the application
start_app() {
    log "Starting $APP_NAME..."
    
    # Check if Python is available
    if ! command -v "$PYTHON_CMD" > /dev/null 2>&1; then
        error "Python 3 not found. Please install Python 3 and tkinter."
        exit 1
    fi
    
    # Check if tkinter is available
    if ! "$PYTHON_CMD" -c "import tkinter" > /dev/null 2>&1; then
        error "tkinter not available. Please install python3-tk."
        exit 1
    fi
    
    # Check if main application file exists
    if [ ! -f "$APP_DIR/screen_machine.py" ]; then
        error "Main application file not found: $APP_DIR/screen_machine.py"
        exit 1
    fi
    
    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Start the application in background
    cd "$APP_DIR"
    nohup "$PYTHON_CMD" screen_machine.py > "$LOG_FILE" 2>&1 &
    APP_PID=$!
    
    # Save PID
    echo "$APP_PID" > "$PID_FILE"
    
    # Wait a moment to check if it started successfully
    sleep 2
    if ps -p "$APP_PID" > /dev/null 2>&1; then
        log "$APP_NAME started successfully with PID $APP_PID"
        info "Log file: $LOG_FILE"
        info "PID file: $PID_FILE"
        return 0
    else
        error "Failed to start $APP_NAME"
        rm -f "$PID_FILE"
        exit 1
    fi
}

# Stop the application
stop_app() {
    if check_running; then
        PID=$(cat "$PID_FILE")
        log "Stopping $APP_NAME (PID: $PID)..."
        kill "$PID" 2>/dev/null || true
        
        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! ps -p "$PID" > /dev/null 2>&1; then
                break
            fi
            sleep 1
        done
        
        # Force kill if still running
        if ps -p "$PID" > /dev/null 2>&1; then
            warning "Force killing $APP_NAME..."
            kill -9 "$PID" 2>/dev/null || true
        fi
        
        rm -f "$PID_FILE"
        log "$APP_NAME stopped"
    else
        log "$APP_NAME is not running"
    fi
}

# Restart the application
restart_app() {
    log "Restarting $APP_NAME..."
    stop_app
    sleep 2
    start_app
}

# Show status
show_status() {
    if check_running; then
        PID=$(cat "$PID_FILE")
        log "$APP_NAME is running (PID: $PID)"
        info "Log file: $LOG_FILE"
        info "PID file: $PID_FILE"
        
        # Show recent log entries
        if [ -f "$LOG_FILE" ]; then
            echo ""
            info "Recent log entries:"
            tail -n 10 "$LOG_FILE" | sed 's/^/  /'
        fi
    else
        log "$APP_NAME is not running"
    fi
}

# Show logs
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        if command -v less > /dev/null 2>&1; then
            less -R "$LOG_FILE"
        else
            cat "$LOG_FILE"
        fi
    else
        log "No log file found"
    fi
}

# Main script logic
case "${1:-start}" in
    start)
        if check_running; then
            warning "$APP_NAME is already running"
            show_status
        else
            start_app
        fi
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the application"
        echo "  stop    - Stop the application"
        echo "  restart - Restart the application"
        echo "  status  - Show application status"
        echo "  logs    - Show application logs"
        echo ""
        echo "Examples:"
        echo "  $0 start    # Start the application"
        echo "  $0 status   # Check if running"
        echo "  $0 logs     # View logs"
        exit 1
        ;;
esac
