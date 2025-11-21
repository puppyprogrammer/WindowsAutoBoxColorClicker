@echo off
REM Attempt to launch silently using pythonw
start "" pythonw main.py

REM If that fails (e.g. pythonw not in path), fall back to visible python
if %errorlevel% neq 0 (
    echo Silent launch failed. Falling back to debug mode...
    python main.py
    pause
)
