import os
import json
import requests
from .base_sampler import BaseSampler
from eval_types import MessageList

class OpenRouterSampler(BaseSampler):
    def __init__(
        self,
        model: str = "meta-llama/llama-3.1-8b-instruct",
        api_key: str = None,
        base_url: str = "https://openrouter.ai/api/v1",
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.base_url = base_url
        self.model = model
        
        # Optional headers defaults
        self.site_url = os.getenv("YOUR_SITE_URL", "http://localhost:3000")
        self.app_name = os.getenv("YOUR_APP_NAME", "SimpleQA-Eval")

    def _pack_message(self, role: str, content: str) -> dict:
        return {"role": str(role), "content": content}

    def __call__(self, message_list: MessageList) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.site_url,
            "X-Title": self.app_name,
        }

        payload = {
            "model": self.model,
            "messages": message_list,
            "top_p": 1,
            "temperature": 0.65,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "repetition_penalty": 1,
            "top_k": 0,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                data=json.dumps(payload)
            )
            
            if response.status_code != 200:
                print(f"Error response: {response.status_code} - {response.text}")
                raise Exception(f"API request failed: {response.text}")

            return response.json()["choices"][0]["message"]["content"]
            
        except Exception as e:
            print(f"Error calling OpenRouter API: {str(e)}")
            print(f"Request headers: {headers}")
            print(f"Request payload: {json.dumps(payload, indent=2)}")
            raise
