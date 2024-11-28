import os
from openai import OpenAI
from .base_sampler import BaseSampler
from eval_types import MessageList

class OpenRouterSampler(BaseSampler):
    def __init__(
        self,
        model: str,
        api_key: str = None,
        base_url: str = "https://openrouter.ai/api/v1",
        temperature: float = 0.5,
        max_tokens: int = 1024,
    ):
        self.client = OpenAI(
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
            base_url=base_url,
        )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _pack_message(self, role: str, content: str) -> dict:
        return {"role": str(role), "content": content}

    def __call__(self, message_list: MessageList) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message_list,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
