# Task Scheduler Setup for Full WhisperWriter Functionality

## The Problem
Task Scheduler by default runs in a restricted session that can't:
- Type text into applications
- Copy to clipboard  
- Interact with your desktop
- Access the system tray

## The Solution: User Session Context

Configure Task Scheduler to run WhisperWriter in your actual user session.

## Step-by-Step Setup

### 1. Open Task Scheduler
- Press `Win + R` → type `taskschd.msc` → Enter

### 2. Create Task (Advanced)
- Click **"Create Task..."** (NOT "Create Basic Task")
- Name: `WhisperWriter Startup`

### 3. General Tab Settings
- ✅ **"Run only when user is logged on"** (CRITICAL!)
- ✅ **"Run with highest privileges"**
- ❌ **DO NOT** check "Run whether user is logged on or not"
- Configure for: **Windows 10**

### 4. Triggers Tab
- Click **"New..."**
- Begin the task: **"At startup"**
- ✅ **"Enabled"**
- **Advanced Settings**:
  - ✅ **"Delay task for: 30 seconds"** (gives system time to load)

### 5. Actions Tab
- Click **"New..."**
- Action: **"Start a program"**
- **Program/script**: `C:\Users\svile\Desktop\github-repos\whisper-writer\start_whisperwriter.bat`
- **Start in**: `C:\Users\svile\Desktop\github-repos\whisper-writer`

### 6. Conditions Tab
- ❌ **Uncheck** "Start the task only if the computer is on AC power"
- ❌ **Uncheck** "Stop if the computer switches to battery power"

### 7. Settings Tab
- ✅ **"Allow task to be run on demand"**
- ✅ **"Run task as soon as possible after a scheduled start is missed"**
- ❌ **Uncheck** "Stop the task if it runs longer than"

## Alternative: Startup Folder Method

If Task Scheduler still has issues, use the Windows Startup folder:

### Method 1: Direct Shortcut
1. Press `Win + R` → type `shell:startup` → Enter
2. Copy `start_whisperwriter.bat` to this folder
3. Rename it to `WhisperWriter.bat`

### Method 2: VBScript Wrapper
1. Press `Win + R` → type `shell:startup` → Enter  
2. Copy `start_whisperwriter_hidden.vbs` to this folder
3. Rename it to `WhisperWriter.vbs`

## Testing Your Setup

### Test the Task
1. In Task Scheduler, right-click your task → **"Run"**
2. Wait 30-60 seconds for WhisperWriter to load
3. Look for the WhisperWriter icon in your system tray
4. Test your hotkey (`Ctrl+Shift+E`)
5. Try recording and see if text appears where you want it

### Check if Working
- ✅ System tray icon appears
- ✅ Hotkey triggers recording  
- ✅ Text gets typed into active application
- ✅ Text copied to clipboard (if enabled)
- ✅ Status window appears (if not hidden)

## Troubleshooting

### If text isn't being typed:
- Make sure you're using `start_whisperwriter.bat` (not the headless version)
- Check Task Scheduler settings: "Run only when user is logged on"
- Try the Startup Folder method instead

### If no system tray icon:
- Task is probably running in background session
- Use "Run only when user is logged on" setting
- Add longer delay (60 seconds) in trigger settings

### If hotkey doesn't work:
- Check that only one WhisperWriter instance is running
- Look for error messages in the console window
- Try running the batch file manually first

## Why This Works

**User Session Context**: Running "when user is logged on" gives WhisperWriter:
- Full desktop access
- Ability to send keystrokes to applications
- Clipboard access
- System tray integration
- All GUI functionality

**Background Session**: Running "whether user is logged on or not" restricts access:
- No desktop interaction
- No clipboard access
- No system tray
- Limited functionality (headless mode problems)

## Security Note

This method requires you to be logged in for WhisperWriter to work. This is normal and necessary for desktop interaction functionality. 