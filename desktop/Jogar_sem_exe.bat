@echo off
cd /d "%~dp0"
python -m pip install --quiet matplotlib >nul 2>&1
start "" pythonw pyquest.py
