import requests
from typing import List, Dict


class LocalLLMClient:
    def __init__(
        self,
        base_url: str = "http://localhost:4891/v1/chat/completions",
        model: str = "Nous Hermes 2 Mistral DPO",
        temperature: float = 0.7,
        max_tokens: int = 512,
    ):
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def chat(self, messages: List[Dict[str, str]]) -> str:

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

        resp = requests.post(
            self.base_url,
            json=payload,
            timeout=120,
        )

        resp.raise_for_status()
        data = resp.json()

        # GPT4All returns OpenAI-style responses:
        # { "choices": [ { "message": { "role": "assistant", "content": "..." } } ] }
        try:
            return data["choices"][0]["message"]["content"]
        except Exception:
            return "⚠️ GPT4All returned an unexpected response format."
