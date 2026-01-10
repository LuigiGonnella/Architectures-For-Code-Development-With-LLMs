# Quick Start Guide

## Prerequisites
- Python 3.12+ with virtual environment activated
- Node.js 18+ and npm
- Ollama running locally with qwen2.5-coder:7b-instruct model

## Setup (First Time Only)

### Backend Setup
```bash
cd single_agent_webapp/backend
pip install -r requirements.txt
```

### Frontend Setup
```bash
cd single_agent_webapp/frontend
npm install
```

## Running the Application

### Option 1: Using Batch Scripts (Windows)

**Start Backend:**
```bash
cd single_agent_webapp/backend
start_backend.bat
```

**Start Frontend:**
```bash
cd single_agent_webapp/frontend
start_frontend.bat
```

### Option 2: Manual Start

**Backend (Port 8000):**
```bash
cd single_agent_webapp/backend
set PYTHONPATH=D:\PersonalStudy\projects\LLM-for-SE
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend (Port 3000):**
```bash
cd single_agent_webapp/frontend
npm run dev
```

## Access the Application

- **Web Interface:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Environment Variables

### Backend (.env)
```
OPENAI_API_KEY=your_key_if_using_openai
MODEL_NAME=qwen2.5-coder:7b-instruct
PORT=8000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Troubleshooting

- **Import Errors:** Make sure PYTHONPATH includes the project root
- **Port Conflicts:** Check if ports 3000 or 8000 are already in use
- **Ollama Not Running:** Start Ollama and pull the model: `ollama pull qwen2.5-coder:7b-instruct`
