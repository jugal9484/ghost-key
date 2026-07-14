@echo off
REM Ghost Key launcher for Windows
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
    python -m password_toolkit %*
) else (
    py -3 -m password_toolkit %*
)
endlocal
