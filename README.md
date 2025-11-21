# AutoBox Color Clicker
A simple Python tool to automate clicking on a specific color within a selected screen region.

## Setup
1.  Ensure Python is installed.
2.  Run `run.bat` to start the application.
    - If it fails, you may need to install dependencies manually: `pip install -r requirements.txt`

## How to Use
1.  **Region Selection**: Click **"1. New Selection Region"**. Drag a box around the area you want to monitor.
2.  **Color Selection**: Click **"2. Pick Color"**. Click on the specific pixel on your screen that you want the bot to target.
3.  **Start**: Click **"3. Start"** to begin monitoring.
    - The bot will scan the selected region. When it sees the target color, it will click it.
4.  Click **"Stop"** to pause.

## Troubleshooting
- **"System cannot find the path specified"**: This usually means Python is not in your system PATH.
    - When installing Python, make sure to check **"Add Python to PATH"**.
    - Or, you can edit `run.bat` to point to your specific python.exe location.
- **Not clicking?** Try increasing the tolerance in `bot.py` or re-picking the color to ensure it matches exactly.
- **Clicking wrong thing?** Your region might be too big or the color too common. Try a smaller, more specific region.
