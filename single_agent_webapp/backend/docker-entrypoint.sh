#!/bin/sh

echo ""
echo "Backend API starting..."
echo ""
echo "Access the services at:"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs:    http://localhost:8000/docs"
echo "  - Frontend:    http://localhost:3000"
echo ""

exec uvicorn main:app --host 0.0.0.0 --port 8000

