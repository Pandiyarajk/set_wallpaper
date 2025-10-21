"""
Windows Desktop Wallpaper Rotator - Continuous Mode

This script continuously rotates your Windows desktop wallpaper at regular intervals.
It runs in the foreground and changes wallpapers in a loop until stopped by the user.

Features:
- Continuous wallpaper rotation while script is running
- Random selection from configured image folder
- Configurable interval via desktop_wallpaper.config file
- Supports multiple image formats (jpg, jpeg, png, bmp)
- Uses default values if config file is not found
- Graceful shutdown with Ctrl+C

Usage:
    python set_desktop.py
    
    Press Ctrl+C to stop the rotation

Requirements:
    - Windows OS
    - desktop_wallpaper.config file (optional - uses defaults if not found)

Note:
    This script runs continuously in the foreground. For background/scheduled changes,
    use schedule_wallpaper.py instead, which integrates with Windows Task Scheduler.
"""

import os
import sys
import subprocess
import time
from glob import glob
import random
import configparser

# ================= DEFAULT CONFIGURATION =================

# Default settings used when config file is not found
DEFAULT_CONFIG = {
    'image_folder': os.path.dirname(os.path.abspath(__file__)),  # Script's directory
    'interval_minutes': 30,  # 30 minute default
    'extensions': ['jpg', 'jpeg', 'png', 'bmp']
}

# ================= CONFIGURATION LOADING =================

def load_config():
    """
    Load configuration settings from desktop_wallpaper.config file.
    If the config file is not found, uses default values instead.
    
    Returns:
        dict: Configuration dictionary with all settings
        
    Note:
        This function will NOT exit if config file is missing - it uses defaults instead.
        Only exits if config file exists but is malformed.
    """
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'desktop_wallpaper.config')
    
    # Check if config file exists
    if not os.path.exists(config_path):
        print(f"⚠️  Config file not found: desktop_wallpaper.config")
        print(f"📋 Using default settings:")
        print(f"   - Image folder: {DEFAULT_CONFIG['image_folder']}")
        print(f"   - Interval: {DEFAULT_CONFIG['interval_minutes']} minute(s)")
        print(f"   - Formats: {', '.join(DEFAULT_CONFIG['extensions'])}")
        print()
        return DEFAULT_CONFIG.copy()
    
    # Config file exists - try to read it
    try:
        config.read(config_path)
        
        # Extract configuration values with fallback to defaults
        settings = {
            'image_folder': config.get('Paths', 'image_folder', 
                                      fallback=DEFAULT_CONFIG['image_folder']),
            'interval_minutes': config.getint('Timing', 'interval_minutes', 
                                             fallback=DEFAULT_CONFIG['interval_minutes']),
            'extensions': config.get('ImageFormats', 'extensions', 
                                    fallback=','.join(DEFAULT_CONFIG['extensions'])).split(',')
        }
        
        print(f"✅ Loaded config from: desktop_wallpaper.config")
        return settings
        
    except Exception as e:
        print(f"❌ Error reading desktop_wallpaper.config: {e}")
        print(f"📋 Using default settings instead")
        return DEFAULT_CONFIG.copy()

# Load configuration at module level
CONFIG = load_config()

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
        
    Raises:
        subprocess.CalledProcessError: If PowerShell command fails
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

def get_image_list():
    """
    Retrieve a list of all image files from the configured folder.
    
    Scans the image folder for files matching the configured extensions
    and returns a list of absolute paths.
    
    Returns:
        list: List of absolute paths to image files
    """
    images = []
    for ext in CONFIG['extensions']:
        # Strip whitespace and build glob pattern for each extension
        images.extend(glob(os.path.join(CONFIG['image_folder'], f"*.{ext.strip()}")))
    return images

# ================= MAIN EXECUTION =================

def main():
    """
    Main execution loop for continuous wallpaper rotation.
    
    This function continuously rotates wallpapers at the configured interval
    until interrupted by the user (Ctrl+C). Each iteration:
    1. Gets list of available images
    2. Randomly selects one image
    3. Sets it as wallpaper
    4. Waits for the configured interval (in minutes)
    5. Repeats
    
    The loop runs indefinitely until KeyboardInterrupt (Ctrl+C) is received.
    """
    # Get initial list of images and validate
    images = get_image_list()
    if not images:
        print(f"❌ No images found in folder: {CONFIG['image_folder']}")
        print(f"   Supported formats: {', '.join(CONFIG['extensions'])}")
        return

    # Convert minutes to seconds for sleep function
    interval_seconds = CONFIG['interval_minutes'] * 60
    
    # Display startup information
    print(f"🖼️  Found {len(images)} images in {CONFIG['image_folder']}")
    print(f"⏱️  Rotation interval: {CONFIG['interval_minutes']} minute(s) ({interval_seconds} seconds)")
    print(f"🔄 Starting wallpaper rotation... (Press Ctrl+C to stop)")
    print("-" * 60)

    try:
        # Main rotation loop - runs until interrupted
        while True:
            # Randomly select an image from the list
            image = random.choice(images)
            
            # Set the selected image as wallpaper
            set_wallpaper(image)
            
            # Display confirmation with timestamp
            timestamp = time.strftime("%H:%M:%S")
            print(f"[{timestamp}] ✅ Set wallpaper: {os.path.basename(image)}")
            
            # Wait for the configured interval before next change (convert minutes to seconds)
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        # Graceful shutdown when user presses Ctrl+C
        print("\n" + "-" * 60)
        print("🛑 Wallpaper rotation stopped by user.")
        print("   Current wallpaper will remain set.")

if __name__ == "__main__":
    main()
