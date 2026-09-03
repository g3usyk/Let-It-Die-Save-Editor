@echo off
chcp 65001 >nul
title LET IT DIE - Save Editor
echo Starting LET IT DIE Save Editor...
python editor_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Installing dependencies...
    pip install -r requirements.txt
    python editor_gui.py
)
