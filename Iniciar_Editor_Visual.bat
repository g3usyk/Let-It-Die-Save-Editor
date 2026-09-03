@echo off
title LET IT DIE - Save Editor GUI
cd /d "%~dp0"
python -m pip install -q -r requirements.txt >nul 2>&1
python editor_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Error al iniciar la interfaz gráfica. Presiona una tecla para salir.
    pause >nul
)
