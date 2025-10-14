# 🚀 Quick Start Guide

## For End Users (First Time Setup)

### Step 1: Get Docker Desktop
Download and install Docker Desktop: https://www.docker.com/products/docker-desktop/

### Step 2: Run the Setup Wizard

**Windows:**
```powershell
.\easy-setup.ps1
```

**Mac/Linux:**
```bash
./easy-setup.sh
```

### Step 3: Enter API Keys
The wizard will help you get FREE API keys from:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://makersuite.google.com/app/apikey
- Grok: https://x.ai/api (optional)
- Perplexity: https://www.perplexity.ai/settings/api (optional)

### Step 4: Start Chatting! 🎉
The app will automatically open at http://localhost:5173

---

## Daily Use (After Setup)

### Start the App
```bash
docker-compose up -d
```

Then open: http://localhost:5173

### Stop the App
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

---

## Troubleshooting

### "Docker is not running"
Start Docker Desktop from your Applications

### "Port already in use"
Edit `.env` file and change the port numbers

### "API key error"
Check your `.env` file - make sure API keys are correct

### Services won't start
```bash
# Reset everything and start fresh
docker-compose down -v
docker-compose up -d
```

---

## Quick Commands Reference

| Action | Command |
|--------|---------|
| Start app | `docker-compose up -d` |
| Stop app | `docker-compose down` |
| View logs | `docker-compose logs -f` |
| Restart | `docker-compose restart` |
| Check status | `docker-compose ps` |
| Full reset | `docker-compose down -v` |

---

## URLs

- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/api/v1/docs
- **Health Check**: http://localhost:8000/health

---

## Need More Help?

- Full guide: `README.md`
- Detailed setup: `complete_setup_guide.md`
- Docker help: `DOCKER_README.md`

---

**That's it! Enjoy chatting with multiple AI models! 🤖💬**

