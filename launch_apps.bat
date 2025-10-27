@echo off
echo Starting your daily setup...

:: Launch Microsoft Edge
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

:: Launch Mozilla Firefox
start "" "C:\Program Files\Mozilla Firefox\firefox.exe"

:: Launch Slack
start "" "C:\Users\%USERNAME%\AppData\Local\slack\slack.exe"

:: Launch Microsoft Teams (new version)
start "" "C:\Users\%USERNAME%\AppData\Local\Microsoft\Teams\Update.exe" --processStart "ms-teams.exe"

:: Launch Notepad
start "" notepad.exe

:: Launch Visual Studio Code
start "" "C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe"

:: Open File Explorer (e.g., Documents folder)
start "" explorer.exe "C:\Users\%USERNAME%\Downloads"

echo All apps launched successfully!
pause
