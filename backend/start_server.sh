#!/bin/bash
# Start the FastAPI development server

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment and start server
echo "🚀 Starting Team 4 Assessment & Quiz Agent Backend..."
echo "📍 Server will run at: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""

./venv/bin/python -m uvicorn app.main:app --reload --port 8000
