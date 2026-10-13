Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Get the directory where this VBS file is located
scriptDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Change to the script directory (critical for batch file to find venv and run.py)
objShell.CurrentDirectory = scriptDir

' Run the working batch file with no window (0 = hidden, False = don't wait)
' This preserves all GUI functionality (typing, clipboard, system tray) while hiding the console
objShell.Run Chr(34) & scriptDir & "\start_whisperwriter.bat" & Chr(34), 0, False

Set objShell = Nothing
Set objFSO = Nothing 