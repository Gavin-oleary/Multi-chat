#!/bin/bash

# Multi-Model Chat Client - Start Script
# This script starts both backend and frontend in separate terminals

echo "🚀 Starting Multi-Model Chat Client..."
echo ""

# Check if backend .env exists
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env not found!"
    echo "Please copy backend/.env.example to backend/.env and configure your API keys."
    exit 1
fi

# Check if frontend .env exists
if [ ! -f "frontend/.env" ]; then
    echo "⚠️  Warning: frontend/.env not found. Creating from example..."
    cp frontend/.env.example frontend/.env
fi

# Function to start backend
start_backend() {
    echo "📦 Starting Backend..."
    cd backend
    
    # Check if venv exists
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python -m venv venv
    fi
    
    # Activate venv
    source venv/bin/activate
    
    # Install dependencies
    pip install -q -r requirements.txt
    
    # Initialize database if needed
    python init_db.py
    
    # Start backend server
    echo "✅ Backend starting on http://localhost:8000"
    python -m app.main
}

# Function to start frontend
start_frontend() {
    echo "🎨 Starting Frontend..."
    cd frontend
    
    # Install dependencies if needed
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi
    
    # Start frontend server
    echo "✅ Frontend starting on http://localhost:5173"
    npm run dev
}

# Detect OS and start in separate terminals
case "$(uname -s)" in
    Darwin*)    # macOS
        osascript -e 'tell application "Terminal" to do script "cd \"'$PWD'\" && ./start.sh backend"'
        osascript -e 'tell application "Terminal" to do script "cd \"'$PWD'\" && ./start.sh frontend"'
        ;;
    Linux*)     # Linux
        if command -v gnome-terminal &> /dev/null; then
            gnome-terminal -- bash -c "cd '$PWD' && ./start.sh backend; exec bash"
            gnome-terminal -- bash -c "cd '$PWD' && ./start.sh frontend; exec bash"
        elif command -v xterm &> /dev/null; then
            xterm -e "cd '$PWD' && ./start.sh backend" &
            xterm -e "cd '$PWD' && ./start.sh frontend" &
        else
            echo "Please install gnome-terminal or xterm, or run backend and frontend manually"
            exit 1
        fi
        ;;
    *)
        # If terminal type detection fails or manual mode
        if [ "$1" = "backend" ]; then
            start_backend
        elif [ "$1" = "frontend" ]; then
            start_frontend
        else
            echo "Starting in manual mode..."
            echo ""
            echo "Please run these commands in separate terminals:"
            echo ""
            echo "Terminal 1 (Backend):"
            echo "  cd backend"
            echo "  source venv/bin/activate"
            echo "  python -m app.main"
            echo ""
            echo "Terminal 2 (Frontend):"
            echo "  cd frontend"
            echo "  npm run dev"
        fi
        ;;
esac

echo ""
echo "✅ Setup complete!"
echo "📖 Backend API Docs: http://localhost:8000/api/v1/docs"
echo "🌐 Frontend App: http://localhost:5173"