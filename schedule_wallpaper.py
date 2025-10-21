"""
Windows Wallpaper Changer with Task Scheduler Integration

This script automatically changes your Windows desktop wallpaper at scheduled intervals
using Windows Task Scheduler. It randomly selects images from a configured folder and
sets them as the desktop background.

Features:
- Automatically creates a Windows Task Scheduler task
- Randomly selects wallpapers from a specified folder
- Configurable interval via config.ini file
- Supports multiple image formats (jpg, jpeg, png, bmp)

Usage:
    python schedule_wallpaper.py

Requirements:
    - Windows OS
    - Administrator privileges (for Task Scheduler)
    - config.ini file in the same directory
"""

import os
import sys
import subprocess
from glob import glob
import random
import configparser

# ================= CONFIGURATION LOADING =================

def load_config():
    """
    Load configuration settings from config.ini file.
    
    Returns:
        dict: Configuration dictionary with all settings
        
    Raises:
        SystemExit: If config.ini is not found or cannot be parsed
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
    
    if not os.path.exists(config_path):
        print(f"❌ Error: config.ini not found at {config_path}")
        print("Please create a config.ini file in the same directory as this script.")
        sys.exit(1)
    
    try:
        config.read(config_path)
        
        # Extract configuration values with defaults
        settings = {
            'image_folder': config.get('Paths', 'image_folder'),
            'python_exe': config.get('Paths', 'python_exe'),
            'interval_minutes': config.getint('Timing', 'interval_minutes', fallback=30),
            'task_name': config.get('TaskScheduler', 'task_name', fallback='WallpaperChanger'),
            'extensions': config.get('ImageFormats', 'extensions', fallback='jpg,jpeg,png,bmp').split(',')
        }
        
        return settings
    except Exception as e:
        print(f"❌ Error reading config.ini: {e}")
        sys.exit(1)

# Load configuration at module level
CONFIG = load_config()
SCRIPT_PATH = os.path.abspath(__file__)  # Full path to this script

# ================= WALLPAPER FUNCTIONS =================

def set_wallpaper(image_path):
    """
    Set the Windows desktop wallpaper using PowerShell and SystemParametersInfo API.
    
    This function uses the Windows user32.dll SystemParametersInfo function to change
    the desktop wallpaper. The change is immediate and persistent across reboots.
    
    Args:
        image_path (str): Absolute path to the image file to set as wallpaper
        
    Technical Details:
        - uAction=20 (SPI_SETDESKWALLPAPER): Sets the desktop wallpaper
        - fuWinIni=3 (SPIF_UPDATEINIFILE | SPIF_SENDCHANGE): Updates user profile and broadcasts change
    """
    # PowerShell command that defines and calls the SystemParametersInfo API
    ps_command = f'''
    $code = @"
    using System;
    using System.Runtime.InteropServices;
    public class Wallpaper {{
        [DllImport("user32.dll", SetLastError=true)]
        public static extern bool SystemParametersInfo(int uAction,int uParam,string lpvParam,int fuWinIni);
    }}
"@; Add-Type $code; [Wallpaper]::SystemParametersInfo(20, 0, "{image_path}", 3)
    '''
    subprocess.run(["powershell", "-Command", ps_command], check=True)

def choose_and_set_wallpaper():
    """
    Select a random image from the configured folder and set it as wallpaper.
    
    This function scans the image folder for all supported image formats,
    randomly selects one, and sets it as the desktop wallpaper.
    
    Returns:
        bool: True if wallpaper was set successfully, False otherwise
    """
    # Build list of all image files matching configured extensions
    images = []
    for ext in CONFIG['extensions']:
        images.extend(glob(os.path.join(CONFIG['image_folder'], f"*.{ext.strip()}")))
    
    if not images:
        print(f"❌ No images found in folder: {CONFIG['image_folder']}")
        print(f"   Supported formats: {', '.join(CONFIG['extensions'])}")
        return False

    # Randomly select an image and set it as wallpaper
    image = random.choice(images)
    set_wallpaper(image)
    print(f"✅ Set wallpaper: {os.path.basename(image)}")
    return True

# ================= TASK SCHEDULER FUNCTIONS =================

def create_task():
    """
    Create a Windows Task Scheduler task to run this script at regular intervals.
    
    This function creates a scheduled task that runs with HIGHEST privileges to ensure
    the wallpaper can be changed even when the user is not logged in. The task runs
    at the interval specified in config.ini.
    
    The task is created with the following properties:
    - Trigger: Time-based (every N minutes)
    - Action: Run Python script with full path
    - Run Level: Highest (administrator)
    - Force: Overwrites existing task if present
    """
    # Check if task already exists to avoid duplicates
    result = subprocess.run(
        ["schtasks", "/Query", "/TN", CONFIG['task_name']], 
        capture_output=True, 
        text=True
    )
    
    if "ERROR:" not in result.stdout:
        print(f"✅ Task '{CONFIG['task_name']}' already exists. Skipping creation.")
        return

    # Build the schtasks command to create the scheduled task
    # /SC MINUTE /MO N: Run every N minutes
    # /TN: Task name
    # /TR: Task to run (Python executable + script path)
    # /F: Force creation (overwrite if exists)
    # /RL HIGHEST: Run with highest privileges
    command = (
        f'schtasks /Create /SC MINUTE /MO {CONFIG["interval_minutes"]} '
        f'/TN "{CONFIG["task_name"]}" /TR "\\"{CONFIG["python_exe"]}\\" \\"{SCRIPT_PATH}\\"" /F /RL HIGHEST'
    )
    
    subprocess.run(command, shell=True)
    print(f"🎉 Task '{CONFIG['task_name']}' created to run every {CONFIG['interval_minutes']} minutes.")

# ================= MAIN EXECUTION =================

if __name__ == "__main__":
    # Step 1: Create or verify the Task Scheduler task exists
    create_task()
    
    # Step 2: Set a wallpaper immediately on this run
    choose_and_set_wallpaper()
