.PHONY: help install setup start stop clean test docker-up docker-down

help:
	@echo "Multi-Model Chat Client - Available Commands:"
	@echo ""
	@echo "  make install      - Install all dependencies (backend + frontend)"
	@echo "  make setup        - Complete setup (install + database)"
	@echo "  make start        - Start both backend and frontend"
	@echo "  make stop         - Stop all running processes"
	@echo "  make clean        - Remove all build artifacts"
	@echo "  make test         - Run all tests"
	@echo "  make docker-up    - Start with Docker Compose"
	@echo "  make docker-down  - Stop Docker containers"
	@echo ""

install:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Installation complete!"

setup: install
	@echo "Setting up environment files..."
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; fi
	@if [ ! -f frontend/.env ]; then cp frontend/.env.example frontend/.env; fi
	@echo "Initializing database..."
	cd backend && . venv/bin/activate && python init_db.py
	@echo "✅ Setup complete!"
	@echo ""
	@echo "⚠️  Remember to configure your API keys in backend/.env"

start:
	@echo "Starting Multi-Model Chat Client..."
	@echo "Run these commands in separate terminals:"
	@echo ""
	@echo "Terminal 1 (Backend):"
	@echo "  cd backend && source venv/bin/activate && python -m app.main"
	@echo ""
	@echo "Terminal 2 (Frontend):"
	@echo "  cd frontend && npm run dev"

stop:
	@echo "Stopping all processes..."
	@pkill -f "python -m app.main" || true
	@pkill -f "vite" || true
	@echo "✅ Stopped!"

clean:
	@echo "Cleaning build artifacts..."
	rm -rf backend/venv
	rm -rf backend/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf frontend/node_modules
	rm -rf frontend/dist
	rm -rf frontend/.vite
	@echo "✅ Cleaned!"

test:
	@echo "Running backend tests..."
	cd backend && . venv/bin/activate && pytest
	@echo "Running frontend tests..."
	cd frontend && npm run test
	@echo "✅ Tests complete!"

docker-up:
	@echo "Starting with Docker Compose..."
	docker-compose up -d
	@echo "✅ Containers started!"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down
	@echo "✅ Containers stopped!"

backend:
	cd backend && . venv/bin/activate && python -m app.main

frontend:
	cd frontend && npm run dev