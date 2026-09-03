@echo off
chcp 65001 >nul
cd /d "%~dp0\.."
title Compilador de LET IT DIE Save Editor (.EXE)
echo ========================================================
echo       COMPILANDO LET IT DIE SAVE EDITOR A .EXE
echo ========================================================
echo.
python build_exe.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo ≠COMPILACI‡N EXITOSA!
    echo El ejecutable est† listo en la carpeta "dist\LetItDieSaveEditor"
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo ERROR: Fall¢ la compilaci¢n. Revisa los mensajes arriba.
    echo ========================================================
)
pause
