@echo off
title Screen Machine - Wake-on-LAN
echo Starting Screen Machine Wake-on-LAN Utility...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.9+ and try again.
    pause
    exit /b 1
)

REM Check if the Python script exists
if not exist "wake_on_lan_gui.py" (
    echo Error: wake_on_lan_gui.py not found in the current directory.
    echo Please make sure you're running this from the correct folder.
    pause
    exit /b 1
)

REM Check if the core wake_on_lan.py exists
if not exist "wake_on_lan.py" (
    echo Error: wake_on_lan.py not found in the current directory.
    echo Please make sure you copied both wake_on_lan_gui.py and wake_on_lan.py.
    pause
    exit /b 1
)

REM Run the GUI
echo Launching Wake-on-LAN GUI...
python wake_on_lan_gui.py

REM Check if the script ran successfully
if errorlevel 1 (
    echo.
    echo An error occurred while running the Wake-on-LAN utility.
    pause
)

echo.
echo Wake-on-LAN utility finished.
pause
