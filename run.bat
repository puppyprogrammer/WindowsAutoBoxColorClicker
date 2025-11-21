@echo off
REM Use Python to find pythonw and launch the app silently
python -c "import sys, os, subprocess; pythonw = sys.executable.replace('python.exe', 'pythonw.exe'); subprocess.Popen([pythonw, 'main.py'], cwd=os.getcwd())"

if %errorlevel% neq 0 (
    echo.
    echo Launch failed. Trying visible mode...
    python main.py
    pause
)
