# Backend Setup Guide - Quick Start

## 🚀 Complete Setup Instructions

### Step 1: Install PostgreSQL

#### macOS (using Homebrew):
```bash
brew install postgresql@15
brew services start postgresql@15
```

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Windows:
Download and install from [PostgreSQL Downloads](https://www.postgresql.org/download/windows/)

### Step 2: Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Inside psql, create the database:
CREATE DATABASE multimodel_chat;

# Create a user (optional, recommended for production):
CREATE USER chatuser WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE multimodel_chat TO chatuser;

# Exit psql
\q
```

### Step 3: Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` and add your configuration:

```env
# Database - Update with your PostgreSQL credentials
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/multimodel_chat

# API Keys - Get these from the respective providers
ANTHROPIC_API_KEY=sk-ant-xxxxx
OPENAI_API_KEY=sk-xxxxx
GOOGLE_API_KEY=xxxxx
XAI_API_KEY=xxxxx
PERPLEXITY_API_KEY=pplx-xxxxx

# Application Settings
ENVIRONMENT=development
DEBUG=True
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Server
HOST=0.0.0.0
PORT=8000
```

### Step 5: Initialize Database

```bash
# Run the initialization script
python init_db.py
```

You should see:
```
🔧 Initializing database...
📋 Existing tables: []
✅ Database tables created successfully!
📊 Current tables: ['conversations', 'messages']
   ✓ conversations table created
   ✓ messages table created

🎉 Database initialization complete!
```

### Step 6: Run the Server

```bash
# Using the main app
python -m app.main

# OR using uvicorn directly with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
🚀 Multi-Model Chat Client started successfully!
📖 Docs available at: http://0.0.0.0:8000/api/v1/docs
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 7: Test the API

Open your browser and visit:
- API Documentation: http://localhost:8000/api/v1/docs
- Alternative Docs: http://localhost:8000/api/v1/redoc
- Health Check: http://localhost:8000/health

## 📋 API Key Setup

### Getting API Keys:

1. **Anthropic (Claude)**
   - Visit: https://console.anthropic.com/
   - Sign up and create an API key

2. **OpenAI (ChatGPT)**
   - Visit: https://platform.openai.com/api-keys
   - Create a new secret key

3. **Google (Gemini)**
   - Visit: https://makersuite.google.com/app/apikey
   - Create an API key

4. **X.AI (Grok)**
   - Visit: https://x.ai/api
   - Sign up and get API access

5. **Perplexity**
   - Visit: https://www.perplexity.ai/settings/api
   - Generate API key

## 🧪 Testing the Setup

### Using the Interactive Docs:

1. Go to http://localhost:8000/api/v1/docs
2. Click on "POST /api/v1/chat/"
3. Click "Try it out"
4. Enter a test request:
```json
{
  "prompt": "What is the capital of France?",
  "conversation_id": null,
  "models": null
}
```
5. Click "Execute"

You should get responses from all 5 AI models!

### Using curl:

```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello! Tell me a fun fact.",
    "conversation_id": null,
    "models": null
  }'
```

## 🔧 Troubleshooting

### Database Connection Issues:

```bash
# Check if PostgreSQL is running
# macOS:
brew services list | grep postgresql

# Linux:
sudo systemctl status postgresql

# Test connection
psql -U postgres -d multimodel_chat -c "SELECT 1;"
```

### Module Import Errors:

```bash
# Make sure you're in the backend directory and venv is activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### API Key Issues:

- Verify your `.env` file has all keys
- Check that there are no extra spaces or quotes around keys
- Ensure the `.env` file is in the `backend` directory

### Port Already in Use:

```bash
# Change port in .env or run with different port
uvicorn app.main:app --reload --port 8001
```

## 📂 File Checklist

Make sure all these files exist and are not empty:

### Core Files:
- ✅ `requirements.txt` - Python dependencies
- ✅ `.env` - Your environment variables
- ✅ `.env.example` - Example configuration
- ✅ `alembic.ini` - Database migration config

### Application Files:
- ✅ `app/main.py` - FastAPI application entry
- ✅ `app/config.py` - Settings and configuration
- ✅ `app/database.py` - Database setup

### Models:
- ✅ `app/models/conversation.py`
- ✅ `app/models/message.py`
- ✅ `app/models/user.py`

### API Endpoints:
- ✅ `app/api/v1/router.py`
- ✅ `app/api/v1/conversations.py`
- ✅ `app/api/v1/messages.py`
- ✅ `app/api/v1/chat.py`

### Services:
- ✅ `app/services/chat_service.py`
- ✅ `app/services/conversation_service.py`

### AI Clients:
- ✅ `app/clients/base.py`
- ✅ `app/clients/claude.py`
- ✅ `app/clients/openai.py`
- ✅ `app/clients/gemini.py`
- ✅ `app/clients/grok.py`
- ✅ `app/clients/perplexity.py`

## 🎯 Next Steps

Once the backend is running successfully:

1. ✅ Test all endpoints in the API docs
2. ✅ Create a few test conversations
3. ✅ Verify all 5 AI models respond correctly
4. 🔜 Move on to frontend development

## 📝 Notes

- The empty folders `tests/test_services`, `tests/test_clients`, and `alembic/versions` are intentional
- All `__init__.py` files should exist (can be empty)
- Database migrations via Alembic are optional but recommended for production