from abc import ABC, abstractmethod
from typing import List, Dict, AsyncGenerator, Optional


class BaseAIClient(ABC):
    """
    Abstract base class for all AI provider clients.
    Each provider (Claude, ChatGPT, etc.) must implement these methods.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    async def generate_response(self, prompt: str, conversation_history: List[Dict[str, str]] = None, system_prompt: str = None) -> str:
        """
        Generate a response from the AI model.
        
        Args:
            prompt: The user's input prompt
            conversation_history: List of previous messages in format [{"role": "user", "content": "..."}, ...]
            system_prompt: Optional system prompt to set context and behavior
        
        Returns:
            The model's response as a string
        
        Raises:
            Exception: If the API call fails
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Return the specific model name/version being used.
        
        Returns:
            String identifying the model (e.g., "claude-3-opus-20240229")
        """
        pass
    
    def format_conversation_history(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Format conversation history for the specific provider's API format.
        Can be overridden by subclasses if they need special formatting.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
        
        Returns:
            Formatted message list for the provider
        """
        return messages
    
    async def generate_stream(
        self, 
        prompt: str, 
        conversation_history: List[Dict[str, str]] = None
    ) -> AsyncGenerator[str, None]:
        """
        Stream response from the AI model.
        
        This is an optional method - if not implemented, the system will
        fall back to the regular generate_response method.
        
        Args:
            prompt: The user's input prompt
            conversation_history: List of previous messages
            
        Yields:
            Chunks of the response as they become available
        """
        # Default implementation: just yield the complete response
        response = await self.generate_response(prompt, conversation_history)
        yield response