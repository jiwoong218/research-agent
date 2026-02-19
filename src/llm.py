import requests
from typing import Optional


class LLMClient:
    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "llama3.2"
    ):
        self.base_url = base_url
        self.model = model

    def chat(self, messages: list[dict], tools: Optional[list] = None) -> dict:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        if tools:
            payload["tools"] = tools

        response = requests.post(f"{self.base_url}/api/chat", json=payload)
        response.raise_for_status()
        return response.json()

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
