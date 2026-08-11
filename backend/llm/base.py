from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass