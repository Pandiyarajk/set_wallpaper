# Windows Desktop Wallpaper Changer

A lightweight Python solution for automatically changing your Windows desktop wallpaper. Choose between continuous rotation or scheduled changes using Windows Task Scheduler.

## 🌟 Features

- **Two Operation Modes:**
  - **Continuous Mode** (`set_desktop.py`): Runs in foreground with real-time rotation
  - **Scheduled Mode** (`schedule_wallpaper.py`): Integrates with Windows Task Scheduler for background operation
- **Random Selection**: Randomly picks wallpapers from your image folder
- **Multiple Format Support**: Works with JPG, JPEG, PNG, and BMP images
- **Configurable Settings**: Easy configuration via `config.ini` file
- **Graceful Operation**: Clean startup and shutdown with informative messages

## 📋 Requirements

- **Operating System**: Windows 10 or later
- **Python**: Python 3.6 or higher
- **Privileges**: Administrator rights (for Task Scheduler integration only)

## 🚀 Quick Start

### 1. Setup Configuration

Edit the `config.ini` file to customize your settings:

```ini
[Paths]
# Set your wallpaper folder path
image_folder = C:\Users\YourName\Pictures\Wallpapers

# Set your Python executable path
python_exe = C:\Python313\python.exe

[Timing]
# Scheduled mode interval (minutes)
interval_minutes = 30

[TaskScheduler]
# Task name in Windows Task Scheduler
task_name = WallpaperChanger

[ImageFormats]
# Supported image formats (comma-separated)
extensions = jpg,jpeg,png,bmp
```

### 2. Add Your Images

Place your wallpaper images in the folder specified in `config.ini`:

```
C:\Users\YourName\Pictures\Wallpapers\
  ├── wallpaper1.jpg
  ├── wallpaper2.png
  ├── wallpaper3.jpg
  └── ...
```

### 3. Choose Your Mode

#### Option A: Continuous Mode (Foreground)

Run the script manually for continuous rotation:

```bash
python set_desktop.py
```

- Runs in the foreground
- Changes wallpaper every N seconds (configured in `config.ini`)
- Press `Ctrl+C` to stop
- Perfect for active sessions where you want frequent changes

#### Option B: Scheduled Mode (Background)

Set up automatic background rotation with Task Scheduler:

```bash
python schedule_wallpaper.py
```

- Creates a Windows Task Scheduler task automatically
- Runs in the background at configured intervals
- Changes wallpaper even when you're not logged in
- Perfect for "set it and forget it" operation

## 📖 Detailed Usage

### Continuous Mode (`set_desktop.py`)

**Purpose**: Continuously rotate wallpapers while the script is running.

**How it works:**
1. Loads configuration from `config.ini`
2. Scans the image folder for supported formats
3. Enters an infinite loop that:
   - Randomly selects an image
   - Sets it as wallpaper
   - Waits for the configured interval
   - Repeats

**When to use:**
- You want frequent wallpaper changes during active work sessions
- You prefer manual control over when rotation starts/stops
- You don't want to set up Task Scheduler

**Example Output:**
```
🖼️  Found 25 images in C:\Users\YourName\Pictures\Wallpapers
⏱️  Rotation interval: 60 seconds
🔄 Starting wallpaper rotation... (Press Ctrl+C to stop)
------------------------------------------------------------
[14:30:15] ✅ Set wallpaper: sunset.jpg
[14:31:15] ✅ Set wallpaper: mountain.png
[14:32:15] ✅ Set wallpaper: ocean.jpg
```

### Scheduled Mode (`schedule_wallpaper.py`)

**Purpose**: Set up automatic wallpaper changes using Windows Task Scheduler.

**How it works:**
1. Loads configuration from `config.ini`
2. Creates a Windows Task Scheduler task (if it doesn't exist)
3. Sets one wallpaper immediately
4. Task Scheduler runs the script at configured intervals

**When to use:**
- You want wallpapers to change automatically in the background
- You want changes to happen even when not logged in
- You prefer less frequent changes (e.g., every 30 minutes or hourly)

**Example Output:**
```
🎉 Task 'WallpaperChanger' created to run every 30 minutes.
✅ Set wallpaper: landscape.jpg
```

**Managing the Task:**

To view the scheduled task:
```bash
schtasks /Query /TN WallpaperChanger
```

To delete the scheduled task:
```bash
schtasks /Delete /TN WallpaperChanger /F
```

To run the task manually:
```bash
schtasks /Run /TN WallpaperChanger
```

## ⚙️ Configuration Reference

### `config.ini` Sections

#### `[Paths]`
- **`image_folder`**: Absolute path to your wallpaper folder
  - Example: `C:\Users\YourName\Pictures\Wallpapers`
  - Must be a valid directory path
  
- **`python_exe`**: Full path to your Python executable
  - Example: `C:\Python313\python.exe`
  - Required for Task Scheduler integration
  - Find yours with: `where python` in Command Prompt

#### `[Timing]`
- **`interval_minutes`**: Rotation interval for `schedule_wallpaper.py` (scheduled mode)
  - Default: `30` (30 minutes)
  - Range: Any positive integer
  - Windows Task Scheduler minimum is 1 minute

#### `[TaskScheduler]`
- **`task_name`**: Name of the Windows Task Scheduler task
  - Default: `WallpaperChanger`
  - Must be unique in Task Scheduler
  - Appears in Task Scheduler Library

#### `[ImageFormats]`
- **`extensions`**: Comma-separated list of supported image formats
  - Default: `jpg,jpeg,png,bmp`
  - No spaces between extensions
  - Case-insensitive

## 🔧 Troubleshooting

### "config.ini not found"
**Problem**: The script can't find the configuration file.

**Solution**: 
- Ensure `config.ini` is in the same directory as the Python scripts
- Check that the filename is exactly `config.ini` (not `config.ini.txt`)

### "No images found in folder"
**Problem**: The script can't find any images in the specified folder.

**Solution**:
- Verify the `image_folder` path in `config.ini` is correct
- Check that your images have supported extensions (jpg, jpeg, png, bmp)
- Ensure the folder contains at least one image file

### Task Scheduler task not working
**Problem**: The scheduled task was created but wallpaper doesn't change.

**Solution**:
- Run Command Prompt as Administrator
- Verify the task exists: `schtasks /Query /TN WallpaperChanger`
- Check the `python_exe` path in `config.ini` is correct
- Ensure the image folder path is accessible to the system account

### PowerShell errors
**Problem**: Errors related to PowerShell execution.

**Solution**:
- Ensure PowerShell is available on your system (default on Windows 10+)
- Check that image paths don't contain special characters that break PowerShell
- Try running PowerShell as Administrator

### Wallpaper doesn't persist after reboot
**Problem**: Wallpaper reverts after restarting Windows.

**Solution**:
- This shouldn't happen as the script uses persistent API calls
- Check Windows Settings > Personalization > Background isn't set to "Slideshow"
- Ensure Windows isn't managed by group policy that overrides wallpaper

## 📁 Project Structure

```
set_desktop_image/
├── config.ini                  # Scheduled configuration file
├── desktop_wallpaper.config    # Continuous mode configuration
├── set_desktop.py              # Continuous mode script
├── schedule_wallpaper.py       # Scheduled mode script
├── README.md                   # This file
├── 1.jpg                       # Sample wallpaper
└── 2.jpg                       # Sample wallpaper
```

## 🔍 How It Works

Both scripts use the Windows `SystemParametersInfo` API to change the desktop wallpaper. This is the same method Windows uses internally, ensuring compatibility and persistence.

**Technical Details:**
- **API**: `user32.dll` → `SystemParametersInfo` function
- **Action**: `SPI_SETDESKWALLPAPER` (uAction=20)
- **Flags**: `SPIF_UPDATEINIFILE | SPIF_SENDCHANGE` (fuWinIni=3)
- **Method**: PowerShell with C# interop for API access

## 💡 Tips & Best Practices

1. **Image Organization**: Keep wallpapers in a dedicated folder for easy management
2. **Image Resolution**: Use images that match or exceed your screen resolution for best quality
3. **Interval Selection**: 
   - Continuous mode: 30-120 seconds works well for active sessions
   - Scheduled mode: 15-60 minutes prevents distraction
4. **Performance**: Both scripts are lightweight and use minimal system resources
5. **Testing**: Run `set_desktop.py` first to verify your setup before using scheduled mode

## 🆘 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Verify your `config.ini` settings are correct
3. Ensure you have the required permissions (Administrator for Task Scheduler)
4. Test with a small set of images first

## 📝 License

This project is provided as-is for personal use. Feel free to modify and distribute.

## 🤝 Contributing

Suggestions and improvements are welcome! This is a simple utility designed to be easily customizable.

---

**Enjoy your dynamic desktop! 🎨**

