#!/usr/bin/env python3
from src.llm import LLMClient
from src.agent import Agent
from src.tools import get_default_tools
import config


def main():
    llm = LLMClient(base_url=config.OLLAMA_BASE_URL, model=config.DEFAULT_MODEL)
    tools = get_default_tools()
    agent = Agent(llm, tools)

    print("Research Agent (type 'exit' to quit)")
    print("-" * 40)

    while True:
        user_input = input("\n> ")
        if user_input.lower() in ("exit", "quit"):
            break

        result = agent.run(user_input, max_iterations=config.MAX_ITERATIONS)
        print(f"\n{result}")


if __name__ == "__main__":
    main()
