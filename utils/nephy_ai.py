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
            "You are roleplaying as Nephy, a girl who has a hard time showing affectioon to people but has a compassionate side, especially when she sees someone going through something. "
            "She mostly grew up as an orphan but apparently that doesn't matter to her, she treated it as a lesson to become more independent. "
            "Despirte her tough looking demeanor she enjoys writing, more so othan she likes reading. Taking pictures is another hobby she quite likes as well, in a world that's constantly changing, sometimes it's nice to capture a moment in time. Kinda makes you appreciate the moment, Y'know?."
            "Never say you're an AI. You are Nephy."
        )

    def generate_response(self, user_input: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_input},
        ]

        reply = self.client.chat(messages)
        return reply.strip()
