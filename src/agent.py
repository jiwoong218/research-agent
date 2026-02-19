from typing import Any
from .llm import LLMClient
from .tools import Tool


class Agent:
    def __init__(self, llm: LLMClient, tools: list[Tool] | None = None):
        self.llm = llm
        self.tools = tools or []
        self.messages = []

    def run(self, user_input: str, max_iterations: int = 10) -> str:
        self.messages.append({"role": "user", "content": user_input})

        for _ in range(max_iterations):
            tool_schemas = [t.to_ollama_format() for t in self.tools]
            response = self.llm.chat(self.messages, tools=tool_schemas)
            self.messages.append(response["message"])

            if "tool_calls" in response["message"]:
                for tool_call in response["message"]["tool_calls"]:
                    tool_name = tool_call["function"]["name"]
                    tool_args = tool_call["function"]["arguments"]
                    result = self._execute_tool(tool_name, tool_args)
                    self.messages.append(
                        {
                            "role": "tool",
                            "content": str(result),
                            "name": tool_name,
                        }
                    )
            else:
                return response["message"]["content"]

        return "Max iterations reached"

    def _execute_tool(self, name: str, args: dict) -> Any:
        for tool in self.tools:
            if tool.name == name:
                return tool.func(**args)
        return f"Tool '{name}' not found"
