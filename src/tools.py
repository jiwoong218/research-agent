import requests
from bs4 import BeautifulSoup
import inspect
from typing import Any, Callable
from datetime import datetime


class Tool:
    def __init__(self, name: str, description: str, func: Callable):
        self.name = name
        self.description = description
        self.func = func

    def to_ollama_format(self) -> dict:
        sig = inspect.signature(self.func)
        properties = {}
        required = []
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            properties[param_name] = {"type": "string"}
            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        }


class WebSearch(Tool):
    def __init__(self):
        super().__init__(
            name="web_search",
            description="Search the web for information. Returns search results with titles and snippets.",
            func=self._search,
        )

    def _search(self, query: str) -> list[dict]:
        return [
            {
                "error": "Web search temporarily unavailable. Try using web_fetch with a specific URL."
            }
        ]


class WebFetch(Tool):
    def __init__(self):
        super().__init__(
            name="web_fetch",
            description="Fetch the content of a webpage. Returns the text content of the page.",
            func=self._fetch,
        )

    def _fetch(self, url: str, max_length: int = 8000) -> str:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ResearchAgent/1.0)"}
        response = requests.get(url, headers=headers, timeout=10, verify=False)
        response.raise_for_status()
        text = response.text
        text = text[:max_length]
        return f"Fetched from {url}:\n{text}"


class FileRead(Tool):
    def __init__(self):
        super().__init__(
            name="file_read",
            description="Read the contents of a file from the local filesystem.",
            func=self._read,
        )

    def _read(self, path: str) -> str:
        with open(path, "r") as f:
            return f.read()


class FileWrite(Tool):
    def __init__(self):
        super().__init__(
            name="file_write",
            description="Write content to a file on the local filesystem.",
            func=self._write,
        )

    def _write(self, path: str, content: str) -> str:
        with open(path, "w") as f:
            f.write(content)
        return f"Successfully wrote to {path}"


class CurrentTime(Tool):
    def __init__(self):
        super().__init__(
            name="current_time",
            description="Get the current date and time.",
            func=self._get_time,
        )

    def _get_time(self) -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_default_tools() -> list[Tool]:
    return [
        WebSearch(),
        WebFetch(),
        FileRead(),
        FileWrite(),
        CurrentTime(),
    ]
