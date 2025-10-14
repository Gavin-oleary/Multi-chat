# Multi-Model Chat Backend

FastAPI backend for the Multi-Model Chat Client that orchestrates communication with multiple AI providers.

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL Database

Install PostgreSQL and create a database:

```bash
# Using PostgreSQL command line
createdb multimodel_chat

# Or using psql
psql -U postgres
CREATE DATABASE multimodel_chat;
```

### 4. Configure Environment Variables

Copy the example environment file and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```
DATABASE_URL=postgresql://user:password@localhost:5432/multimodel_chat
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
XAI_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
```

### 5. Run the Application

```bash
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- Main API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/api/v1/docs`
- ReDoc: `http://localhost:8000/api/v1/redoc`

## API Endpoints

### Conversations

- `POST /api/v1/conversations/` - Create a new conversation
- `GET /api/v1/conversations/` - List all conversations
- `GET /api/v1/conversations/{id}` - Get a specific conversation with messages
- `PATCH /api/v1/conversations/{id}` - Update conversation (rename)
- `DELETE /api/v1/conversations/{id}` - Delete conversation

### Chat

- `POST /api/v1/chat/` - Send a prompt to all models

Example request:

```json
{
  "prompt": "What is the capital of France?",
  "conversation_id": null,
  "models": null
}
```

Example response:

```json
{
  "conversation_id": 1,
  "user_message_id": 1,
  "responses": [
    {
      "provider": "claude",
      "content": "The capital of France is Paris.",
      "error": null,
      "latency_ms": 523.4
    },
    {
      "provider": "chatgpt",
      "content": "Paris is the capital of France.",
      "error": null,
      "latency_ms": 612.1
    }
  ]
}
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── clients/         # AI provider clients
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── tests/               # Test files
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black app/
flake8 app/
```

### Database Migrations (Optional - using Alembic)

```bash
# Initialize Alembic (already done)
alembic init alembic

# Create a migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Notes

- The database tables are created automatically on first run
- All AI models are called in parallel for faster responses
- Failed model responses are returned with error messages
- Conversation history is maintained for context-aware responses