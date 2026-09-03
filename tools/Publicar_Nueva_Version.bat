@echo off
title LET IT DIE - Publicar Nueva Version en GitHub
cd /d "%~dp0"
python publish_version.py
pause
