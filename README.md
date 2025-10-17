# Multi-Model Chat Client

A powerful chat application that queries multiple AI models simultaneously and compares their responses side-by-side. Chat with Claude, ChatGPT, Gemini, Grok, and Perplexity all at once!

## Features

- 🤖 **5 AI Models**: Compare responses from Claude, ChatGPT, Gemini, Grok, and Perplexity
- 💬 **Conversation Management**: Create, rename, and organize conversations
- 📄 **Document Upload**: Chat with your documents (PDF, DOCX, TXT)
- 🎨 **Modern UI**: Beautiful, responsive interface built with React and Tailwind CSS
- ⚡ **Real-time Responses**: Parallel API calls for fast results
- 🔍 **RAG Support**: Retrieval-Augmented Generation with PostgreSQL pgvector
- 📝 **System Prompts**: Customize AI behavior with pre-defined or custom system prompts

## Quick Start (Recommended)

### Prerequisites

- **Docker Desktop** ([Download](https://www.docker.com/products/docker-desktop))
- **API Keys** from AI providers (all offer free tiers!)

### Easy Installation (Automated)

1. **Clone or download this repository**

2. **Run the setup script**

   **Windows:**
   ```powershell
   .\easy-setup.ps1
   ```

   **Mac/Linux:**
   ```bash
   chmod +x easy-setup.sh
   ./easy-setup.sh
   ```

3. **Follow the prompts** to add your API keys

   The script will guide you through:
   - ✅ Checking Docker installation
   - ✅ Creating the `.env` configuration file
   - ✅ Adding API keys for the providers you want
   - ✅ Starting all containers
   - ✅ Verifying everything is running

4. **Done!** The application will automatically start 🎉

   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/v1/docs

### Manual Installation (Alternative)

If you prefer to set up manually:

1. **Create your environment file**
   ```bash
   cp env.example .env
   ```

2. **Edit `.env` and add your API keys**
   ```env
   OPENAI_API_KEY=your_actual_key_here
   ANTHROPIC_API_KEY=your_actual_key_here
   # ... etc
   ```

3. **Start the application**
   ```bash
   docker compose up -d
   ```

## Usage

### Starting the Application

After the initial setup, you can start the application with:

```bash
docker compose up -d
```

### Stopping the Application

```bash
docker compose down
```

### Restarting the Application

```bash
docker compose restart
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f frontend
```

## Getting API Keys

All providers offer **free API keys** with generous free tiers:

| Provider | Get Your Key | Free Tier |
|----------|-------------|-----------|
| **OpenAI** | [platform.openai.com/api-keys](https://platform.openai.com/api-keys) | $5 free credits |
| **Anthropic** | [console.anthropic.com](https://console.anthropic.com/) | $5 free credits |
| **Google** | [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey) | 60 requests/min |
| **Grok** | [x.ai/api](https://x.ai/api) | Varies |
| **Perplexity** | [perplexity.ai/settings/api](https://www.perplexity.ai/settings/api) | Limited free tier |

💡 **Tip**: You only need API keys for the models you want to use. Start with just one or two!

## Manual Setup (Without Docker)

If you prefer not to use Docker, see [complete_setup_guide.md](complete_setup_guide.md) for detailed manual installation instructions.

## Architecture

```
multi-model-chat/
├── backend/              # FastAPI server
│   ├── app/             # Application code
│   │   ├── api/         # REST API endpoints
│   │   ├── clients/     # AI provider clients
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   └── tests/           # Backend tests
│
├── frontend/            # React app
│   └── src/             # Frontend code
│       ├── components/  # React components
│       ├── hooks/       # Custom hooks
│       ├── pages/       # Page components
│       └── services/    # API client
│
└── docker-compose.yml   # Docker configuration
```

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** with **pgvector** - Database with vector search
- **SQLAlchemy** - ORM
- **Redis** - Caching layer
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client

### AI Providers
- Anthropic Claude
- OpenAI ChatGPT
- Google Gemini
- X.AI Grok
- Perplexity

## Configuration

After setup, you can edit the `.env` file to:
- Update API keys
- Change ports
- Configure CORS origins
- Adjust rate limits

## Features in Detail

### Multi-Model Chat
Ask one question and get responses from all configured AI models simultaneously. Compare their:
- Response quality
- Speed/latency
- Style and tone
- Accuracy

### Document Chat (RAG)
Upload documents and chat with them using Retrieval-Augmented Generation:
- Supports PDF, DOCX, TXT formats
- Automatic text extraction and chunking
- Vector similarity search
- Source attribution

### Conversation Management
- Create multiple conversations
- Rename and organize chats
- Full conversation history
- Delete unwanted conversations

### System Prompts
- Pre-defined prompts for common tasks
- Custom system prompts
- Per-conversation prompt selection

## Troubleshooting

### Docker Issues

**"Docker is not running"**
- Start Docker Desktop from your applications

**"Port already in use"**
- Edit `.env` and change `BACKEND_PORT` or `FRONTEND_PORT`

**"Failed to pull image"**
- Check your internet connection
- Try: `docker compose pull`

### API Issues

**"API key error"**
- Verify your API keys in `.env` file
- Ensure no extra spaces or quotes
- Check that keys are active at the provider's website

**"Rate limit exceeded"**
- You've hit the free tier limit
- Wait for the limit to reset
- Or upgrade to a paid plan with the provider

### General Issues

**"Can't connect to backend"**
- Ensure backend is running: `docker compose ps`
- Check logs: `docker compose logs backend`
- Verify backend is accessible: `curl http://localhost:8000`

**"Frontend not loading"**
- Clear browser cache
- Check logs: `docker compose logs frontend`
- Try accessing directly: http://localhost:5173
- Verify frontend container is running: `docker compose ps`

## Development

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

### Code Formatting

```bash
# Backend
cd backend
black app/
flake8 app/

# Frontend
cd frontend
npm run lint
```

## Deployment

For production deployment instructions, see [deployment.md](deployment.md).

Quick production start:
```bash
docker compose -f docker-compose.prod.yml up -d
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security

- **Never commit your `.env` file** - It contains sensitive API keys
- **Never share your API keys** - They can be abused
- **Rotate keys regularly** - Generate new keys periodically
- **Use environment variables** - Never hardcode secrets

## License

See [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:
- Check the [Troubleshooting](#troubleshooting) section
- Review [complete_setup_guide.md](complete_setup_guide.md)
- Check [DOCKER_README.md](DOCKER_README.md)

## What's Next?

- 🔄 Streaming responses (in progress)
- 🎙️ Voice input support
- 📊 Response analytics and metrics
- 🌐 Multi-language support
- 💾 Export conversations
- 🔌 Plugin system for custom models

---

**Made with ❤️ for the AI community**

Happy chatting! 🚀

