import google.generativeai as genai
from app.clients.base import BaseAIClient
from typing import List, Dict
from app.constants import GEMINI_MODEL


class GeminiClient(BaseAIClient):
    """Client for Google's Gemini API"""
    
    def __init__(self, api_key: str, model: str = GEMINI_MODEL):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model_name = model
        self.model = genai.GenerativeModel(model)
    
    async def generate_response(self, prompt: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from Gemini.
        
        Args:
            prompt: The user's input prompt
            conversation_history: Previous messages in the conversation
        
        Returns:
            Gemini's response as a string
        """
        try:
            # Gemini's API handles conversation history differently
            # We'll need to format it into a chat session or single prompt
            
            if conversation_history:
                # Build context from history
                context = "\n\n".join([
                    f"{msg['role'].capitalize()}: {msg['content']}" 
                    for msg in conversation_history
                ])
                full_prompt = f"{context}\n\nUser: {prompt}\n\nAssistant:"
            else:
                full_prompt = prompt
            
            response = self.model.generate_content(full_prompt)
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Return the Gemini model being used"""
        return self.model_name