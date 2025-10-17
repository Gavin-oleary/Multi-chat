import google.generativeai as genai
from app.clients.base import BaseAIClient
from typing import List, Dict, Optional
from app.constants import GEMINI_MODEL


class GeminiClient(BaseAIClient):
    """Client for Google's Gemini API"""
    
    def __init__(self, api_key: str, model: str = GEMINI_MODEL):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)
    
    async def generate_response(self, prompt: str, conversation_history: Optional[List[Dict[str, str]]] = None, system_prompt: Optional[str] = None) -> str:
        """
        Generate a response from Gemini.
        
        Args:
            prompt: The user's input prompt
            conversation_history: Previous messages in the conversation
            system_prompt: Optional system prompt with RAG context
        
        Returns:
            Gemini's response as a string
        """
        try:
            # Build the full prompt with system prompt and history
            prompt_parts = []
            
            # Add system prompt if provided (includes RAG context)
            if system_prompt:
                prompt_parts.append(f"System Instructions: {system_prompt}\n")
            
            # Add conversation history if provided
            if conversation_history:
                context = "\n\n".join([
                    f"{msg['role'].capitalize()}: {msg['content']}" 
                    for msg in conversation_history
                ])
                prompt_parts.append(context)
            
            # Add current prompt
            prompt_parts.append(f"User: {prompt}\n\nAssistant:")
            
            full_prompt = "\n\n".join(prompt_parts)
            
            response = self.model.generate_content(full_prompt)
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Return the Gemini model being used"""
        return self.model_name