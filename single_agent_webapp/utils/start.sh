#!/bin/bash

# Startup script for LLM-for-SE WebApp
# This script starts both backend and frontend servers

echo "🚀 Starting LLM-for-SE WebApp..."
echo ""

# Check if .env exists in backend
if [ ! -f "../backend/.env" ]; then
    echo "⚠️  Warning: backend/.env not found!"
    echo "Please copy backend/.env.example to backend/.env"
    echo "and configure your settings."
    exit 1
fi

# Start backend in background
echo "📡 Starting FastAPI backend on port 8000..."
export PYTHONPATH="$(pwd)/../.."
cd ../backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ../utils

# Wait a bit for backend to start
sleep 3

# Start frontend
echo ""
echo "🎨 Starting Next.js frontend on port 3000..."
cd ../frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

npm run dev &
FRONTEND_PID=$!
cd ../utils

echo ""
echo "✅ Both servers are starting..."
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Keep script running
wait
