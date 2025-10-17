from anthropic import Anthropic
from app.clients.base import BaseAIClient
from typing import List, Dict, Optional
from app.constants import CLAUDE_MODEL, ERROR_MESSAGES
from app.utils.logging import get_logger

logger = get_logger(__name__)


class ClaudeClient(BaseAIClient):
    """Client for Anthropic's Claude API"""
    
    def __init__(self, api_key: str, model: str = CLAUDE_MODEL):
        super().__init__(api_key)
        self.client = Anthropic(api_key=api_key)
        self.model = model
    
    async def generate_response(self, prompt: str, conversation_history: Optional[List[Dict[str, str]]] = None, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from Claude.
        
        Args:
            prompt: The user's input prompt
            conversation_history: Previous messages in the conversation
            system_prompt: Optional system prompt with RAG context
        
        Returns:
            Claude's response as a string
        """
        messages = []
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add the current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            # Build API call parameters
            params = {
                "model": self.model,
                "max_tokens": 4096,
                "messages": messages
            }
            
            # Add system prompt if provided (includes RAG context)
            if system_prompt:
                params["system"] = system_prompt
            
            response = self.client.messages.create(**params)
            
            # Extract text from response
            return response.content[0].text
        
        except Exception as e:
            logger.error(f"Claude API error: {str(e)}", exc_info=True)
            raise Exception(ERROR_MESSAGES["api_error"].format(error=str(e)))
    
    def get_model_name(self) -> str:
        """Return the Claude model being used"""
        return self.model