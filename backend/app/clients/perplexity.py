import httpx
from app.clients.base import BaseAIClient
from typing import List, Dict
from app.constants import PERPLEXITY_MODEL, PERPLEXITY_API_URL


class PerplexityClient(BaseAIClient):
    """Client for Perplexity AI API"""
    
    def __init__(self, api_key: str, model: str = PERPLEXITY_MODEL):
        super().__init__(api_key)
        self.model = model
        self.base_url = "https://api.perplexity.ai"
    
    async def generate_response(self, prompt: str, conversation_history: List[Dict[str, str]] = None) -> str:
        """
        Generate a response from Perplexity.
        
        Args:
            prompt: The user's input prompt
            conversation_history: Previous messages in the conversation
        
        Returns:
            Perplexity's response as a string
        """
        messages = []
        
        # Perplexity requires a system message
        messages.append({
            "role": "system",
            "content": "Be precise and concise."
        })
        
        # Add conversation history if provided, filtering out any system messages
        # and excluding the last message if it's from the user (to avoid duplicates)
        if conversation_history:
            history_to_add = conversation_history[:]
            # If the last message in history is from user and matches current prompt, skip it
            if history_to_add and history_to_add[-1].get("role") == "user":
                if history_to_add[-1].get("content") == prompt:
                    history_to_add = history_to_add[:-1]
            
            for msg in history_to_add:
                if msg.get("role") != "system":
                    messages.append(msg)
        
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
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,  # Perplexity default
            "top_p": 0.9
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                
                # Log the response for debugging
                if response.status_code != 200:
                    error_detail = response.text
                    print(f"Perplexity API Error: Status {response.status_code}")
                    print(f"Response: {error_detail}")
                    print(f"Request payload: {payload}")
                
                response.raise_for_status()
                
                data = response.json()
                return data["choices"][0]["message"]["content"]
        
        except httpx.HTTPError as e:
            raise Exception(f"Perplexity API error: {str(e)}")
        except Exception as e:
            raise Exception(f"Perplexity client error: {str(e)}")
    
    def get_model_name(self) -> str:
        """Return the Perplexity model being used"""
        return self.model