import os
from openai import OpenAI
from .base_sampler import BaseSampler
from eval_types import MessageList
from prompts.templates import AVAILABLE_PROMPTS
from utils.config import load_config

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

        # Загружаем конфигурацию промптов
        self.config = load_config()
        self.prompt_config = self.config.get("prompts", {})
        self.active_prompt = self.prompt_config.get("active", "none")
        self.custom_prompt = self.prompt_config.get("custom_text")

    def _pack_message(self, role: str, content: str) -> dict:
        if role == "user":
            # Применяем активный промпт
            template = (
                self.custom_prompt if self.active_prompt == "custom" and self.custom_prompt
                else AVAILABLE_PROMPTS.get(self.active_prompt, AVAILABLE_PROMPTS["none"])
            )
            formatted_content = template.format(question=content)
            return {"role": str(role), "content": formatted_content}
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
