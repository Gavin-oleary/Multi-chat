# Complete Setup Guide - Multi-Model Chat Client

This guide will walk you through setting up the entire Multi-Model Chat application from scratch.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9+** installed
- **Node.js 18+** and npm installed
- **PostgreSQL 13+** installed and running
- API keys for all 5 AI providers (see below)

## 🔑 Getting API Keys

You'll need API keys from these providers:

1. **Anthropic (Claude)**
   - Visit: https://console.anthropic.com/
   - Create account → API Keys → Create Key
   - Copy your API key

2. **OpenAI (ChatGPT)**
   - Visit: https://platform.openai.com/api-keys
   - Create account → Create new secret key
   - Copy your API key

3. **Google (Gemini)**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in → Get API key
   - Copy your API key

4. **X.AI (Grok)**
   - Visit: https://x.ai/api
   - Sign up for API access
   - Copy your API key

5. **Perplexity**
   - Visit: https://www.perplexity.ai/settings/api
   - Create account → Generate API key
   - Copy your API key

## 🗄️ Part 1: Database Setup

### Install PostgreSQL

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download from https://www.postgresql.org/download/windows/

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE multimodel_chat;

# Create user (recommended for production)
CREATE USER chatuser WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE multimodel_chat TO chatuser;

# Exit
\q
```

## 🔧 Part 2: Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env
```

Edit `.env` with your settings:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/multimodel_chat

# API Keys (paste your actual keys here)
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
PORT=8000cd 
```

### 5. Initialize Database

```bash
python init_db.py
```

You should see:
```
✅ Database tables created successfully!
   ✓ conversations table created
   ✓ messages table created
```

### 6. Test Backend

```bash
# Start the server
python -m app.main
```

You should see:
```
🚀 Multi-Model Chat Client started successfully!
📖 Docs available at: http://0.0.0.0:8000/api/v1/docs
```

Open http://localhost:8000/api/v1/docs to verify the API is running.

**Keep this terminal running!** Open a new terminal for frontend setup.

## 🎨 Part 3: Frontend Setup

### 1. Navigate to Frontend Directory

In a **new terminal**:

```bash
cd frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install all React, Vite, and other frontend dependencies.

### 3. Configure Environment

```bash
# Copy example env file
cp .env.example .env
```

The `.env` file should contain:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### 4. Start Development Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

## ✅ Part 4: Verify Everything Works

### 1. Open the Application

Visit http://localhost:5173 in your browser.

You should see:
- The Multi-Model Chat interface
- A sidebar on the left
- A chat input at the bottom
- A welcome message showing all 5 models

### 2. Send a Test Message

1. Type a simple question: "What is 2+2?"
2. Click "Send" or press Enter
3. Watch as all 5 AI models respond

You should see:
- Your question appear in the chat
- 5 response cards, one for each model
- Responses appearing (some faster than others)

### 3. Test Conversation Management

1. Click "New Chat" to start a fresh conversation
2. Send another message
3. Check the sidebar - you should see both conversations listed
4. Click on a conversation to view it
5. Try renaming a conversation (hover and click the edit icon)
6. Try deleting a conversation (hover and click the trash icon)

## 🐛 Troubleshooting

### Backend Issues

**"ModuleNotFoundError"**
```bash
# Make sure venv is activated and dependencies installed
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**"Database connection error"**
```bash
# Check PostgreSQL is running
# macOS:
brew services list | grep postgresql
# Linux:
sudo systemctl status postgresql

# Verify DATABASE_URL in .env is correct
```

**"API key error"**
- Verify all API keys in `.env` are correct
- Make sure there are no extra spaces or quotes
- Test each API key individually at the provider's website

### Frontend Issues

**"Cannot find module"**
```bash
# Delete and reinstall node_modules
rm -rf node_modules package-lock.json
npm install
```

**"Port 5173 already in use"**
```bash
# Kill the process using port 5173
# macOS/Linux:
lsof -ti:5173 | xargs kill -9
# Windows:
netstat -ano | findstr :5173
taskkill /PID [PID_NUMBER] /F

# Or change the port in vite.config.js
```

**API requests failing**
- Verify backend is running on port 8000
- Check `VITE_API_BASE_URL` in frontend `.env`
- Look at browser console for CORS errors
- Verify CORS_ORIGINS in backend `.env` includes `http://localhost:5173`

## 📁 File Checklist

Make sure these files exist:

### Backend
- ✅ `requirements.txt`
- ✅ `.env` (created from .env.example)
- ✅ `alembic.ini`
- ✅ All Python files in `app/` directory

### Frontend
- ✅ `package.json`
- ✅ `.env` (created from .env.example)
- ✅ All JavaScript/JSX files in `src/` directory
- ✅ `index.html`
- ✅ `vite.config.js`
- ✅ `tailwind.config.js`

## 🚀 Daily Development Workflow

### Starting Work

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m app.main
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### During Development

- Backend changes auto-reload with uvicorn
- Frontend changes auto-reload with Vite HMR
- Check browser console for frontend errors
- Check terminal for backend errors

### Stopping Work

- Press `Ctrl+C` in both terminals
- Backend: `deactivate` to exit venv

## 🎯 What's Next?

Now that everything is working:

1. **Explore the API** - Visit http://localhost:8000/api/v1/docs
2. **Test different prompts** - Try coding questions, creative writing, etc.
3. **Compare responses** - See how different models handle the same question
4. **Customize** - Modify the UI, add features, adjust model parameters

## 📊 Project Structure Overview

```
multi-model-chat/
├── backend/          ← FastAPI server
│   ├── app/         ← Application code
│   ├── tests/       ← Backend tests
│   ├── .env         ← Backend config (you create this)
│   └── requirements.txt
│
└── frontend/        ← React app
    ├── src/         ← Frontend code
    ├── .env         ← Frontend config (you create this)
    └── package.json
```

## 🔐 Security Notes

- Never commit `.env` files to git
- Keep your API keys secret
- Use environment variables for all secrets
- In production, use proper authentication
- Use HTTPS in production

## 💡 Tips

- Keep both terminals visible to monitor logs
- Use the browser DevTools Network tab to debug API calls
- Check the backend logs for detailed error messages
- The interactive API docs at `/api/v1/docs` are great for testing

## 🆘 Getting Help

If you encounter issues:

1. Check the error message carefully
2. Verify all prerequisites are installed
3. Ensure all environment variables are set correctly
4. Check that both backend and frontend are running
5. Look at browser console and terminal logs

## 🎉 Success!

If you can:
- ✅ Access the app at http://localhost:5173
- ✅ Send a message and get responses from all 5 models
- ✅ Create and manage conversations
- ✅ See the sidebar with conversation history

**Congratulations! Your Multi-Model Chat Client is fully operational!**

Happy chatting! 🚀