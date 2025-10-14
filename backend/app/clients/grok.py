import httpx
from app.clients.base import BaseAIClient
from typing import List, Dict
from app.constants import GROK_MODEL, GROK_API_URL


class GrokClient(BaseAIClient):
    """Client for X.AI's Grok API"""
    
    def __init__(self, api_key: str, model: str = GROK_MODEL):
        super().__init__(api_key)
        self.model = model
        self.base_url = "https://api.x.ai/v1"
    
    async def generate_response(self, prompt: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from Grok.
        
        Args:
            prompt: The user's input prompt
            conversation_history: Previous messages in the conversation
        
        Returns:
            Grok's response as a string
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
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": messages,
            "model": self.model,
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
        
        except httpx.HTTPError as e:
            raise Exception(f"Grok API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Grok client error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Return the Grok model being used"""
        return self.model