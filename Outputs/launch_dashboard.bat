@echo off
title Betting Dashboard Server
echo Starting Betting Dashboard...
echo.

cd /d "%~dp0"

:: Try Python 3
where python >nul 2>&1
if %errorlevel%==0 (
    echo Server running at: http://localhost:8765/betting_dashboard.html
    echo.
    echo DO NOT CLOSE THIS WINDOW while using the dashboard.
    echo Press Ctrl+C to stop the server when done.
    echo.
    start "" "http://localhost:8765/betting_dashboard.html"
    python -m http.server 8765
    goto :end
)

:: Try py launcher
where py >nul 2>&1
if %errorlevel%==0 (
    echo Server running at: http://localhost:8765/betting_dashboard.html
    echo.
    echo DO NOT CLOSE THIS WINDOW while using the dashboard.
    start "" "http://localhost:8765/betting_dashboard.html"
    py -m http.server 8765
    goto :end
)

:: No Python found
echo ERROR: Python not found.
echo.
echo OPTION 1 - Install VS Code Live Server extension:
echo   1. Open VS Code
echo   2. Press Ctrl+Shift+X
echo   3. Search: Live Server  (by Ritwick Dey)
echo   4. Install it
echo   5. Right-click betting_dashboard.html - Open with Live Server
echo.
echo OPTION 2 - Install Python:
echo   Go to https://python.org and install Python 3
echo   Then double-click this file again.
echo.
pause

:end
