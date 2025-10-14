# Deployment Guide

This guide covers various deployment options for the Multi-Model Chat Client.

## Table of Contents

1. [Docker Deployment](#docker-deployment)
2. [Manual Deployment](#manual-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

## Docker Deployment

### Quick Start with Docker Compose

The easiest way to deploy is using Docker Compose:

```bash
# 1. Create a .env file in project root
cat > .env << EOF
DB_PASSWORD=your_secure_password
ANTHROPIC_API_KEY=your_key
OPENAI_API_KEY=your_key
GOOGLE_API_KEY=your_key
XAI_API_KEY=your_key
PERPLEXITY_API_KEY=your_key
EOF

# 2. Start all services
docker-compose up -d

# 3. Check logs
docker-compose logs -f

# 4. Access the application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
```

### Production Docker Setup

For production, modify `docker-compose.yml`:

```yaml
# Use production builds
services:
  backend:
    environment:
      ENVIRONMENT: production
      DEBUG: "False"
  
  frontend:
    build:
      context: ./frontend
      target: production  # Use production Dockerfile stage
```

## Manual Deployment

### Backend Deployment

#### 1. Using Gunicorn (Recommended for Production)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

#### 2. Using Systemd (Linux)

Create `/etc/systemd/system/multimodel-chat.service`:

```ini
[Unit]
Description=Multi-Model Chat Backend
After=network.target postgresql.service

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/multimodel-chat/backend
Environment="PATH=/var/www/multimodel-chat/backend/venv/bin"
ExecStart=/var/www/multimodel-chat/backend/venv/bin/gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable multimodel-chat
sudo systemctl start multimodel-chat
```

### Frontend Deployment

#### Build for Production

```bash
cd frontend
npm run build
```

This creates a `dist/` folder with optimized static files.

#### Serve with Nginx

Create `/etc/nginx/sites-available/multimodel-chat`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        root /var/www/multimodel-chat/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/multimodel-chat /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Cloud Deployment

### Heroku

#### Backend on Heroku

1. Create `Procfile` in backend/:
```
web: gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT
```

2. Deploy:
```bash
heroku create multimodel-chat-backend
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set ANTHROPIC_API_KEY=your_key
heroku config:set OPENAI_API_KEY=your_key
# ... set other keys
git push heroku main
```

#### Frontend on Vercel

```bash
cd frontend
vercel deploy
```

Set environment variable:
- `VITE_API_BASE_URL`: Your Heroku backend URL

### AWS Deployment

#### Backend on EC2

1. Launch EC2 instance (Ubuntu)
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip postgresql nginx
```

3. Clone and setup:
```bash
git clone your-repo
cd multi-model-chat/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Configure systemd (see above)
5. Configure Nginx (see above)

#### Frontend on S3 + CloudFront

1. Build frontend:
```bash
npm run build
```

2. Upload to S3:
```bash
aws s3 sync dist/ s3://your-bucket-name
```

3. Configure CloudFront distribution
4. Update CORS in backend to allow CloudFront domain

### Google Cloud Platform

#### Backend on Cloud Run

1. Create `cloudbuild.yaml`:
```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/multimodel-backend', './backend']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/multimodel-backend']
```

2. Deploy:
```bash
gcloud run deploy multimodel-backend \
  --image gcr.io/PROJECT_ID/multimodel-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Frontend on Firebase Hosting

```bash
cd frontend
npm install -g firebase-tools
firebase login
firebase init hosting
npm run build
firebase deploy
```

## Production Considerations

### Security

1. **HTTPS**: Always use SSL/TLS in production
   - Use Let's Encrypt for free certificates
   - Configure Nginx/Apache for SSL

2. **Environment Variables**: Never commit sensitive data
   - Use secrets management (AWS Secrets Manager, etc.)
   - Rotate API keys regularly

3. **CORS**: Configure proper CORS origins
   ```python
   CORS_ORIGINS=["https://your-domain.com"]
   ```

4. **Rate Limiting**: Implement rate limiting
   ```python
   # Install: pip install slowapi
   from slowapi import Limiter
   ```

5. **Authentication**: Add user authentication
   - JWT tokens
   - OAuth providers
   - Session management

### Performance

1. **Database Connection Pooling**
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=0
   )
   ```

2. **Caching**: Implement Redis for caching
   ```bash
   pip install redis
   ```

3. **CDN**: Use CDN for frontend assets
   - CloudFlare
   - AWS CloudFront
   - Vercel Edge Network

4. **Database Optimization**
   - Add indexes
   - Use connection pooling
   - Regular VACUUM on PostgreSQL

### Monitoring

1. **Logging**: Centralized logging
   ```python
   import logging
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
   )
   ```

2. **Error Tracking**: Use Sentry
   ```bash
   pip install sentry-sdk
   ```

3. **Metrics**: Monitor performance
   - Response times
   - Error rates
   - API usage

4. **Health Checks**: Implement health endpoints
   ```python
   @app.get("/health")
   async def health():
       return {"status": "healthy"}
   ```

### Backup

1. **Database Backups**
   ```bash
   # Automated daily backups
   0 2 * * * pg_dump multimodel_chat > /backups/db_$(date +\%Y\%m\%d).sql
   ```

2. **File Backups**: Backup uploaded files (if any)

3. **Version Control**: All code in Git

### Scaling

1. **Horizontal Scaling**: Multiple backend instances
   - Load balancer (Nginx, AWS ALB)
   - Shared database
   - Session storage (Redis)

2. **Database Scaling**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **Caching Strategy**
   - Redis for sessions
   - CDN for static assets
   - API response caching

### Cost Optimization

1. **API Usage**: Monitor and optimize AI API calls
   - Cache responses when appropriate
   - Implement request throttling
   - Use cheaper models when possible

2. **Infrastructure**
   - Auto-scaling groups
   - Spot instances for non-critical workloads
   - Reserved instances for stable loads

3. **Database**
   - Right-size your database
   - Archive old conversations
   - Regular cleanup

## Environment Variables for Production

```env
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/db
ENVIRONMENT=production
DEBUG=False
CORS_ORIGINS=["https://your-domain.com"]

# API Keys (use secrets manager)
ANTHROPIC_API_KEY=secret
OPENAI_API_KEY=secret
GOOGLE_API_KEY=secret
XAI_API_KEY=secret
PERPLEXITY_API_KEY=secret

# Optional
SENTRY_DSN=your_sentry_dsn
REDIS_URL=redis://localhost:6379
```

## Troubleshooting Production Issues

1. **Check logs first**
   ```bash
   # Docker
   docker-compose logs -f backend
   
   # Systemd
   journalctl -u multimodel-chat -f
   
   # Nginx
   tail -f /var/log/nginx/error.log
   ```

2. **Database connection issues**
   - Verify credentials
   - Check firewall rules
   - Verify SSL settings

3. **High API costs**
   - Implement caching
   - Add rate limiting
   - Monitor usage patterns

4. **Performance issues**
   - Check database queries
   - Review API response times
   - Monitor resource usage

## Support

For deployment issues:
- Check logs
- Review configuration
- Consult cloud provider docs
- Open GitHub issue