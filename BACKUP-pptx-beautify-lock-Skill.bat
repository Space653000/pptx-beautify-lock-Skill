@echo off
setlocal EnableExtensions

set "REPO_URL=https://github.com/Space653000/pptx-beautify-lock-Skill.git"
set "DEST=%~dp0pptx-beautify-lock-Skill"

echo.
echo PPTX Beautify Lock - GitHub Backup
echo Source: %REPO_URL%
echo Target: %DEST%
echo.

where git >nul 2>nul
if errorlevel 1 (
    echo ERROR: git.exe was not found.
    echo Install Git for Windows, then double-click this BAT again.
    pause
    exit /b 1
)

if exist "%DEST%\.git" (
    echo Existing repository found. Updating safely...
    git -C "%DEST%" fetch --all --tags --prune
    if errorlevel 1 goto :fail
    git -C "%DEST%" pull --ff-only
    if errorlevel 1 goto :fail
) else (
    if exist "%DEST%" (
        echo ERROR: Target folder already exists but is not a Git repository.
        echo Rename or delete it, or move this BAT to another folder.
        pause
        exit /b 2
    )
    echo Cloning complete repository...
    git clone "%REPO_URL%" "%DEST%"
    if errorlevel 1 goto :fail
)

echo.
echo BACKUP_OK
echo Saved to: %DEST%
pause
exit /b 0

:fail
echo.
echo BACKUP_FAILED
echo Existing files were not force-overwritten.
pause
exit /b 3
