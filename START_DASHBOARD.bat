@echo off
echo ==========================================
echo   Cucumber Detection Dashboard Launcher
echo ==========================================
echo.
echo [1/2] Activating Environment...
call .venv\Scripts\activate.bat

echo [2/2] Launching Optimzed Dashboard...
echo Dashboard will open in your browser shortly...
streamlit run src/dashboard.py

pause
