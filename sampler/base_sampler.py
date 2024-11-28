from abc import ABC, abstractmethod
from eval_types import MessageList

class BaseSampler(ABC):
    @abstractmethod
    def __call__(self, message_list: MessageList) -> str:
        pass

    @abstractmethod
    def _pack_message(self, role: str, content: str) -> dict:
        pass
