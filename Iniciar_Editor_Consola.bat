@echo off
title LET IT DIE - Save Editor CLI
cd /d "%~dp0"
python editor_cli.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Presiona una tecla para salir.
    pause >nul
)
