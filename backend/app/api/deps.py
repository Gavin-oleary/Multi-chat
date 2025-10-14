from app.config import settings
from app.clients.claude import ClaudeClient
from app.clients.openai import OpenAIClient
from app.clients.gemini import GeminiClient
from app.clients.grok import GrokClient
from app.clients.perplexity import PerplexityClient
from app.models.message import ModelProvider

def get_ai_clients():
    """Initialize and return all AI clients"""
    return {
        ModelProvider.CLAUDE: ClaudeClient(settings.ANTHROPIC_API_KEY),
        ModelProvider.CHATGPT: OpenAIClient(settings.OPENAI_API_KEY),
        ModelProvider.GEMINI: GeminiClient(settings.GOOGLE_API_KEY),
        ModelProvider.GROK: GrokClient(settings.XAI_API_KEY),
        ModelProvider.PERPLEXITY: PerplexityClient(settings.PERPLEXITY_API_KEY),
    }