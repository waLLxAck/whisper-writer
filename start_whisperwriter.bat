@echo off
setlocal

:: Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

:: Change to the project directory
cd /d "%SCRIPT_DIR%"

echo Starting WhisperWriter...
echo Project Directory: %CD%

:: Check if run.py exists
if not exist "run.py" (
    echo ERROR: run.py not found in the project directory
    echo Please make sure you're running this batch file from the correct directory.
    pause
    exit /b 1
)

:: Run the application using virtual environment Python directly
echo Starting WhisperWriter application...
python run.py

:: If the application exits, pause to see any error messages
if errorlevel 1 (
    echo.
    echo Application exited with error code %errorlevel%
    pause
)

endlocal 