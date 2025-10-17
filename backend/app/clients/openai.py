from openai import OpenAI
from app.clients.base import BaseAIClient
from typing import List, Dict, Optional
from app.constants import OPENAI_MODEL


class OpenAIClient(BaseAIClient):
    """Client for OpenAI's ChatGPT API"""
    
    def __init__(self, api_key: str, model: str = OPENAI_MODEL):
        super().__init__(api_key)
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    async def generate_response(self, prompt: str, conversation_history: Optional[List[Dict[str, str]]] = None, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from ChatGPT.
        
        Args:
            prompt: The user's input prompt
            conversation_history: Previous messages in the conversation
            system_prompt: Optional system prompt with RAG context
        
        Returns:
            ChatGPT's response as a string
        """
        messages = []
        
        # Add system prompt if provided (includes RAG context)
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add the current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=4096
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Return the OpenAI model being used"""
        return self.model