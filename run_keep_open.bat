@echo off
setlocal
cd /d "%~dp0"

echo ==============================================
echo IoT AI Cucumber Project - Run (Keep Open)
echo ==============================================

if not exist .venv (
    echo [INFO] Creating virtual environment...
    py -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\setup_and_run.py

echo.
echo ==============================================
echo Run finished. Press any key to close.
echo ==============================================
pause >nul
endlocal
