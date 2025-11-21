@echo off
REM Try running with 'python' command
python main.py
if %errorlevel% equ 0 goto end

REM If that failed, try 'py' launcher
py main.py
if %errorlevel% equ 0 goto end

echo.
echo ========================================================
echo Error: Could not start the application.
echo Python was not found or 'main.py' failed to run.
echo.
echo Please ensure Python is installed and added to your PATH.
echo ========================================================
echo.
pause

:end
