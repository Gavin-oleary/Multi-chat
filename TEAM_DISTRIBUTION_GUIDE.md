# Multi-Model Chat - Team Distribution Guide

## System Requirements

### Minimum Hardware Requirements
- **CPU**: Intel i7-1065G7 or better (4 cores, 8 threads)
- **RAM**: 32GB
- **OS**: Windows 10 or later
- **Storage**: 10GB free space
- **Internet**: Required for AI provider API calls

### Software Prerequisites
1. **Docker Desktop for Windows**
   - Download: https://www.docker.com/products/docker-desktop
   - Enable WSL 2 backend (recommended for better performance)
   - Allocate at least 16GB RAM to Docker in settings

2. **Git** (optional, for cloning)
   - Download: https://git-scm.com/download/win

## Quick Setup Instructions

### Option 1: Easy Setup (Recommended)

1. **Get the Code**
   ```powershell
   git clone <repository-url>
   cd Mulit-chat
   ```

2. **Run the Setup Script**
   ```powershell
   .\easy-setup.ps1
   ```

3. **Follow the Prompts**
   - The script will check Docker
   - Create your `.env` file
   - Ask for your API keys
   - Start all containers
   - Verify everything is running

That's it! The script handles everything automatically. ✨

### Option 2: Manual Setup

1. **Get the Code**
   ```powershell
   git clone <repository-url>
   cd Mulit-chat
   ```

2. **Configure Environment**
   ```powershell
   Copy-Item env.example .env
   notepad .env
   ```
   - Replace placeholder values with actual API keys
   - At minimum, add your `OPENAI_API_KEY`

3. **Start the Application**
   ```powershell
   docker compose up -d
   ```

This will:
- Download required Docker images (first time only)
- Build backend and frontend containers
- Start PostgreSQL database with pgvector
- Start Redis cache
- Run database migrations
- Start all services

**First-time setup takes 5-10 minutes depending on internet speed.**

### Step 4: Access the Application
Once all containers are running:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/v1/docs

## Resource Allocation

The Docker setup is optimized for the minimum hardware requirements:

| Service   | CPU Limit | Memory Limit | CPU Reserved | Memory Reserved |
|-----------|-----------|--------------|--------------|-----------------|
| PostgreSQL| 2 cores   | 4GB          | 1 core       | 2GB             |
| Redis     | 1 core    | 2GB          | 0.5 cores    | 512MB           |
| Backend   | 3 cores   | 8GB          | 1 core       | 2GB             |
| Frontend  | 2 cores   | 4GB          | 0.5 cores    | 1GB             |
| **Total** | **8 cores**| **18GB**    | **3 cores**  | **5.5GB**       |

## Common Commands

### View Service Status
```powershell
docker-compose ps
```

### View Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop Services
```powershell
docker-compose down
```

### Restart Services
```powershell
docker-compose restart
```

### Rebuild After Code Updates
```powershell
docker-compose down
docker-compose build
docker-compose up -d
```

### Complete Reset (removes all data)
```powershell
docker-compose down -v
docker-compose up -d
```

## Features to Test

### 1. Multi-Model Chat
- Create conversations with different AI providers
- Switch between OpenAI, Claude, Gemini, Grok, and Perplexity
- Test streaming responses

### 2. System Prompts
- Navigate to Settings
- Create custom system prompts
- Apply them to conversations
- Test default prompts (Professional, Creative, etc.)

### 3. RAG (Document Chat)
- Upload documents (PDF, TXT, MD, DOC, DOCX)
- Ask questions about uploaded content
- Test with different embedding strategies

### 4. Conversation Management
- Create, rename, and delete conversations
- Search through conversation history
- Export conversation data

## Troubleshooting

### Docker Desktop Not Starting
1. Enable virtualization in BIOS
2. Enable WSL 2: `wsl --install` in PowerShell (Admin)
3. Restart computer

### Port Already in Use
Edit `.env` and change conflicting ports:
```env
POSTGRES_PORT=5433
BACKEND_PORT=8001
FRONTEND_PORT=5174
```

Then restart: `docker-compose down && docker-compose up -d`

### Backend Can't Connect to Database
```powershell
# Check if PostgreSQL is healthy
docker-compose ps

# Check PostgreSQL logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

### Out of Memory Errors
Increase Docker Desktop memory allocation:
1. Open Docker Desktop
2. Settings → Resources
3. Increase Memory to at least 16GB
4. Apply & Restart

### API Keys Not Working
1. Verify keys are correct in `.env`
2. Ensure no extra spaces or quotes
3. Restart backend: `docker-compose restart backend`
4. Check logs: `docker-compose logs backend`

## Testing Checklist

- [ ] Application starts successfully
- [ ] Can access frontend at http://localhost:5173
- [ ] Can create a new conversation
- [ ] Can send messages and receive responses
- [ ] Can switch between AI providers
- [ ] Can upload a document
- [ ] Can ask questions about uploaded documents
- [ ] Can create custom system prompts
- [ ] Can apply system prompts to conversations
- [ ] Streaming responses work properly
- [ ] Conversation history persists after restart

## Feedback & Issues

Please report any issues with:
1. Steps to reproduce
2. Screenshots if applicable
3. Relevant logs: `docker-compose logs > logs.txt`
4. System specifications

## Data Backup (Important!)

To backup your data before updates:
```powershell
docker-compose exec postgres pg_dump -U postgres multichat > backup.sql
```

To restore:
```powershell
docker-compose exec -T postgres psql -U postgres multichat < backup.sql
```

## Updating to New Versions

```powershell
# Stop services
docker-compose down

# Pull latest code (if using git)
git pull

# Rebuild containers
docker-compose build --no-cache

# Start services
docker-compose up -d

# Check logs for any issues
docker-compose logs -f
```

## Performance Tips

1. **Close unused applications** when running the chat application
2. **Use SSD** for Docker data storage if possible
3. **Limit concurrent conversations** to 2-3 for optimal performance
4. **Clear browser cache** if frontend becomes sluggish
5. **Monitor resource usage** in Docker Desktop dashboard

## Security Notes

- **Never commit the `.env` file** to version control
- **Use strong passwords** for database configuration
- **Keep API keys secure** and don't share them
- **Rotate API keys** regularly
- For production deployment, see `deployment.md`

## Support

For detailed documentation, see:
- `README.md` - Project overview
- `DOCKER_README.md` - Advanced Docker usage
- `complete_setup_guide.md` - Comprehensive setup guide
- `QUICK_START.md` - Quick reference guide

