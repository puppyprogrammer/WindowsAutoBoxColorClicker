@echo off
REM Method 1: Try to launch the .pyw file directly (uses Windows File Associations)
REM This is the standard way to run silent Python scripts
start "" "AutoBox.pyw"

REM We can't easily check if 'start' succeeded because it returns immediately.
REM But if Python is installed, .pyw should work.

REM Method 2: Fallback - try 'py' launcher if installed
py --version >nul 2>&1
if %errorlevel% equ 0 (
    REM 'py' launcher handles .pyw files by using pythonw.exe
    start "" py "AutoBox.pyw"
    exit
)

REM Method 3: Fallback - try 'python' command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    REM Use python to find pythonw
    python -c "import sys, os, subprocess; pythonw = sys.executable.replace('python.exe', 'pythonw.exe'); subprocess.Popen([pythonw, 'AutoBox.pyw'], cwd=os.getcwd())"
    exit
)

echo.
echo ==============================================================
echo CRITICAL ERROR: Python not found!
echo.
echo We tried to launch 'AutoBox.pyw' but failed.
echo.
echo 1. Please install Python from python.org
echo 2. IMPORTANT: Check the box "Add Python to PATH" during install.
echo 3. Try double-clicking 'AutoBox.pyw' directly.
echo ==============================================================
echo.
pause
