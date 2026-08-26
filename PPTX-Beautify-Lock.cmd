@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 launcher\pptx_beautify_gui.py
  exit /b %errorlevel%
)
where python >nul 2>nul
if %errorlevel%==0 (
  python launcher\pptx_beautify_gui.py
  exit /b %errorlevel%
)
echo Python 3 was not found.
echo Install Python 3 for Windows, or download the prebuilt PPTX-Beautify-Lock.exe from GitHub Actions artifacts.
pause
exit /b 1
