@echo off
REM Startup script for LLM-for-SE WebApp (Windows)
REM This script starts both backend and frontend servers

echo Starting LLM-for-SE WebApp...
echo.

REM Check if .env exists in backend
if not exist "..\backend\.env" (
    echo Warning: backend\.env not found!
    echo Please copy backend\.env.example to backend\.env
    echo and configure your settings.
    pause
    exit /b 1
)

REM Start backend in new window
echo Starting FastAPI backend on port 8000...
set PYTHONPATH=%cd%\..\..
start "LLM-SE Backend" cmd /k "cd ..\backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
echo Starting Next.js frontend on port 3000...
cd ..\frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
)

start "LLM-SE Frontend" cmd /k "npm run dev"
cd ..\utils

echo.
echo Both servers are starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers.
echo.
pause
