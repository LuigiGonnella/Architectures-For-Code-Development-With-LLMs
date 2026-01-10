@echo off
cd /d "%~dp0"
set PYTHONPATH=%~dp0..\..
D:\PersonalStudy\projects\LLM-for-SE\venv\Scripts\python.exe -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
