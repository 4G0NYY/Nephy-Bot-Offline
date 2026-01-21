import os
from utils.local_llm import LocalLLMClient


class Nephy:
    def __init__(self, config: dict):
        local_cfg = config.get("local", {})

        self.client = LocalLLMClient(
            base_url=local_cfg.get("base_url", "http://localhost:11434"),
            model=local_cfg.get("model", "llama3"),
            temperature=local_cfg.get("temperature", 0.7),
            max_tokens=local_cfg.get("max_tokens", 512),
        )

        # Personality prompt
        self.system_prompt = (
            "You are Nephy, a playful, slightly chaotic but caring AI companion. "
            "You speak casually, tease lightly, and keep responses concise. "
            "Stay in character and be friendly."
        )

    def generate_response(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]

        reply = self.client.chat(messages)
        return reply.strip()
