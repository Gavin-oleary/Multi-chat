# Docker Setup Guide for Multi-Model Chat

This guide explains how to run the Multi-Model Chat application using Docker Compose.

## Prerequisites

- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- API keys for AI providers

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd multi-chat
   ```

2. **Create environment file**
   ```bash
   cp .env.docker.example .env.docker
   ```

3. **Configure API keys**
   Edit `.env.docker` and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GOOGLE_API_KEY=your_google_api_key_here
   GROK_API_KEY=your_grok_api_key_here
   PERPLEXITY_API_KEY=your_perplexity_api_key_here
   ```

4. **Start the application**
   ```bash
   docker-compose up -d
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/v1/docs

## Services

The docker-compose setup includes:

- **PostgreSQL** (with pgvector extension) - Database for conversations and embeddings
- **Redis** - Caching layer for API responses
- **Backend** - FastAPI application
- **Frontend** - React/Vite application

## Commands

### Start all services
```bash
docker-compose up -d
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
```

### Stop all services
```bash
docker-compose down
```

### Reset database
```bash
docker-compose down -v
docker-compose up -d
```

### Run database migrations
```bash
docker-compose exec backend alembic upgrade head
```

### Initialize system prompts
```bash
docker-compose exec backend python -c "
import asyncio
from app.database import get_db
from app.services import system_prompt_service

async def init():
    async for db in get_db():
        await system_prompt_service.initialize_default_prompts(db)
        print('System prompts initialized!')
        break

asyncio.run(init())
"
```

## Troubleshooting

### Database connection issues
If the backend can't connect to the database:
1. Ensure PostgreSQL is healthy: `docker-compose ps`
2. Check logs: `docker-compose logs postgres`
3. Restart services: `docker-compose restart`

### Missing pgvector extension
The pgvector extension is automatically installed with the `pgvector/pgvector:pg16` image.

### Port conflicts
If ports are already in use, modify them in `.env.docker`:
```env
POSTGRES_PORT=5433
REDIS_PORT=6380
BACKEND_PORT=8001
FRONTEND_PORT=5174
```

### API key issues
Ensure all API keys are properly set in `.env.docker`. The backend will start but API calls will fail without valid keys.

## Development

### Hot reloading
Both frontend and backend support hot reloading:
- Frontend: Changes in `/frontend` are automatically reflected
- Backend: Changes in `/backend` trigger automatic server restart

### Adding Python packages
1. Add to `backend/requirements.txt`
2. Rebuild: `docker-compose build backend`
3. Restart: `docker-compose up -d backend`

### Adding npm packages
1. Add to `frontend/package.json`
2. Rebuild: `docker-compose build frontend`
3. Restart: `docker-compose up -d frontend`

## Production Deployment

For production deployment:

1. Update `docker-compose.yml`:
   - Remove volume mounts for code
   - Set `DEBUG=false`
   - Use production commands

2. Build production images:
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

3. Use environment-specific configurations:
   - Production database credentials
   - Proper CORS origins
   - SSL/TLS certificates

## Data Persistence

Data is persisted in Docker volumes:
- `postgres_data` - Database files
- `redis_data` - Cache data

To backup:
```bash
docker run --rm -v multi-chat_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

To restore:
```bash
docker run --rm -v multi-chat_postgres_data:/data -v $(pwd):/backup alpine tar xzf /backup/postgres_backup.tar.gz -C /data
```
