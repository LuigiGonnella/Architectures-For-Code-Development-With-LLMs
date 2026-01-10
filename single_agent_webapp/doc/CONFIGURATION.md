# Single Agent WebApp - Configuration Summary

## ✅ Fixed Issues

### Utils Scripts
- **start.bat & start.sh**: Fixed all paths from `webapp/` to `single_agent_webapp/`
- Updated backend startup to use `python -m uvicorn main:app` with proper PYTHONPATH
- Scripts now correctly reference `../backend` and `../frontend` directories

### Docker Configuration
- **docker-compose.yml**: 
  - Fixed context paths to `../..` (project root)
  - Updated Dockerfile paths to `single_agent_webapp/`
  - Changed model default to `qwen2.5-coder:7b-instruct`
  - Set frontend API URL to `http://backend:8000` for container networking
  
- **Backend Dockerfile**:
  - Fixed paths from `webapp/` to `single_agent_webapp/`
  - Proper WORKDIR set to `/app/single_agent_webapp/backend`
  
- **Frontend Dockerfile**:
  - Fixed paths from `webapp/` to `single_agent_webapp/`
  - Multi-stage build configured correctly

### Health Check
- **health_check.py**: Updated paths in error messages to use `single_agent_webapp/`

## 📁 File Structure

```
single_agent_webapp/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── start_backend.bat
│   └── .env (create from .env.example)
├── frontend/
│   ├── src/
│   ├── package.json
│   ├── Dockerfile
│   ├── start_frontend.bat
│   └── .env.local (created)
└── utils/
    ├── start.bat (Windows startup)
    ├── start.sh (Linux/Mac startup)
    ├── docker-compose.yml
    ├── health_check.py
    ├── .env.example (for Docker)
    ├── requirements.txt (for health_check)
    └── DOCKER.md (Docker guide)
```

## 🚀 Usage Options

### Option 1: Direct Startup (Recommended for Development)
```bash
# Windows
cd single_agent_webapp/backend
start_backend.bat

cd single_agent_webapp/frontend
start_frontend.bat

# Or use the unified scripts
cd single_agent_webapp/utils
start.bat  # Windows
./start.sh # Linux/Mac
```

### Option 2: Docker (Recommended for Production)
```bash
cd single_agent_webapp/utils
cp .env.example .env
# Edit .env with your settings
docker-compose up --build
```

### Option 3: Manual (Full Control)
```bash
# Backend
cd single_agent_webapp/backend
set PYTHONPATH=D:\PersonalStudy\projects\LLM-for-SE
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Frontend (in another terminal)
cd single_agent_webapp/frontend
npm run dev
```

## 🔍 Health Check

```bash
cd single_agent_webapp/utils
pip install -r requirements.txt
python health_check.py
```

## ⚠️ Notes

1. **PYTHONPATH**: Critical for imports - backend needs access to parent project
2. **Ollama**: Must be running if using local models
3. **Ports**: Backend on 8000, Frontend on 3000
4. **Docker**: Use `host.docker.internal` to connect to host Ollama from containers

## 🐛 Known Linting Warnings (Non-Critical)

- `health_check.py`: F-string without placeholders (cosmetic)
- `health_check.py`: High cognitive complexity (works correctly)

These don't affect functionality.
