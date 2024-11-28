import os
from openai import OpenAI
from .base_sampler import BaseSampler
from eval_types import MessageList

class OpenAISampler(BaseSampler):
    def __init__(
        self,
        model: str,
        api_key: str = None,
        system_message: str = None,
        temperature: float = 0.5,
        max_tokens: int = 1024,
    ):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model
        self.system_message = system_message
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _pack_message(self, role: str, content: str) -> dict:
        return {"role": str(role), "content": content}

    def __call__(self, message_list: MessageList) -> str:
        if self.system_message:
            message_list = [self._pack_message("system", self.system_message)] + message_list
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=message_list,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content
