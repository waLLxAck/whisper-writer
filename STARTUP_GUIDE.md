# WhisperWriter Startup Automation Guide

This guide explains how to automatically start WhisperWriter when your PC boots up or run it easily with batch files.

## Files Created

Three automation files have been created for you:

1. **`start_whisperwriter.bat`** - Interactive batch file with console output
2. **`start_whisperwriter_silent.bat`** - Silent batch file that logs to files
3. **`start_whisperwriter_hidden.vbs`** - VBScript that runs completely hidden

## Quick Start

### Manual Execution
- **With console window**: Double-click `start_whisperwriter.bat`
- **Hidden/Silent**: Double-click `start_whisperwriter_hidden.vbs`

## Windows Startup Options

### Option 1: Startup Folder (Easiest)

1. Press `Win + R` to open Run dialog
2. Type `shell:startup` and press Enter
3. Copy `start_whisperwriter_hidden.vbs` to this folder
4. WhisperWriter will start automatically on next boot

### Option 2: Task Scheduler (Most Reliable)

1. Press `Win + R`, type `taskschd.msc`, press Enter
2. Click "Create Basic Task..." in the right panel
3. Name: "WhisperWriter Startup"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: Browse to your `start_whisperwriter_hidden.vbs` file
7. Finish and test

### Option 3: Registry (Advanced Users)

1. Press `Win + R`, type `regedit`, press Enter
2. Navigate to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
3. Right-click → New → String Value
4. Name: "WhisperWriter"
5. Value: Full path to your `start_whisperwriter_hidden.vbs` file

## Troubleshooting

### Check Logs
If the silent version doesn't work, check the logs in the `logs/` directory for error messages.

### Common Issues

1. **Virtual environment not found**: Make sure your `venv` folder exists and contains `Scripts\activate.bat`
2. **Python not found**: Ensure Python is properly installed in your virtual environment
3. **Permission errors**: Run as administrator if needed
4. **Path issues**: Make sure all files are in the correct WhisperWriter project directory

### Manual Testing

Test the automation files manually before setting up startup:

```batch
# Test the interactive version first
start_whisperwriter.bat

# If that works, test the hidden version
start_whisperwriter_hidden.vbs
```

### Disable Startup

To stop WhisperWriter from starting automatically:

- **Startup folder**: Delete the file from `shell:startup`
- **Task Scheduler**: Find and disable/delete the task
- **Registry**: Delete the registry entry

## File Descriptions

### start_whisperwriter.bat
- Shows console window with progress messages
- Pauses on errors so you can see what went wrong
- Good for troubleshooting and manual runs

### start_whisperwriter_silent.bat
- Runs without showing console window
- Logs all output to timestamped files in `logs/` directory
- Good for automated scenarios where you still want logs

### start_whisperwriter_hidden.vbs
- Completely invisible execution
- No console windows or visible processes
- Perfect for Windows startup
- Uses the silent batch file internally

## Prerequisites

Before using these automation files, make sure:

1. ✅ Your virtual environment is set up: `venv/Scripts/activate.bat` exists
2. ✅ All dependencies are installed: `pip install -r requirements.txt`
3. ✅ WhisperWriter runs manually: `python run.py` works in activated venv
4. ✅ Configuration is complete: `src/config.yaml` exists and is configured

## Security Notes

- The VBScript runs with your user permissions
- No elevated privileges are required
- All files remain in your project directory
- Logs are created locally for debugging

## Advanced Configuration

### Delay Startup
If you want to delay startup (useful for slow boot systems), modify the VBScript:

```vb
' Add this line before the objShell.Run command to wait 30 seconds
WScript.Sleep 30000
```

### Change Log Location
Edit `start_whisperwriter_silent.bat` to change where logs are stored:

```batch
:: Change this line to your preferred location
if not exist "C:\logs\whisperwriter" mkdir "C:\logs\whisperwriter"
set "LOG_FILE=C:\logs\whisperwriter\startup_%date:~-4%-%date:~4,2%-%date:~7,2%_%time:~0,2%-%time:~3,2%-%time:~6,2%.log"
```

## Support

If you encounter issues:

1. Check the logs in the `logs/` directory
2. Test manually with `start_whisperwriter.bat` first
3. Ensure your virtual environment is working properly
4. Verify WhisperWriter configuration is complete 