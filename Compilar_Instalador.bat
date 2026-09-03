@echo off
chcp 65001 >nul
title Compilador de Instalador Windows (.EXE)
echo ========================================================
echo   GENERANDO INSTALADOR WINDOWS (SETUP.EXE)
echo ========================================================
echo.
echo 1. Verificando ejecutable compilado...
if not exist "dist\LetItDieSaveEditor\LetItDieSaveEditor.exe" (
    echo Compilando aplicacion base primero...
    python build_exe.py
)

echo 2. Empaquetando instalador con Inno Setup...
"C:\Users\sipi_\AppData\Local\Programs\Inno Setup 6\ISCC.exe" installer.iss

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo ≠INSTALADOR CREADO CON êXITO!
    echo Ubicaci¢n: dist\Instalador_LetItDieSaveEditor_v3.5.exe
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo ERROR: No se pudo generar el instalador.
    echo ========================================================
)
pause
