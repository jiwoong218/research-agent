# Research Agent

An AI-powered research agent built from scratch using Python and Ollama (local LLM).

## Overview

This is an LLM-based research agent that can autonomously search, fetch, and process information from the web and filesystem. It uses the ReAct (Reasoning + Acting) pattern to break down complex research tasks into executable steps.

## Architecture

### Core Components

```
research-agent/
├── config.py          # Configuration (Ollama URL, model, etc.)
├── main.py            # CLI entry point
├── src/
│   ├── __init__.py
│   ├── agent.py       # ReAct agent loop
│   ├── llm.py         # Ollama client
│   └── tools.py       # Tool definitions & implementations
└── pyproject.toml     # Project dependencies (uv)
```

### Tech Stack

- **Language:** Python 3.11+
- **LLM:** Ollama (qwen3:1.7b default)
- **Package Manager:** uv

## Features

### Implemented

| Feature | Description |
|---------|-------------|
| ReAct Loop | Think → Action → Observation cycle |
| Tool System | Extensible tool framework |
| `current_time` | Get current date/time |
| `file_read` | Read local files |
| `file_write` | Write to local files |
| `web_fetch` | Fetch webpage content |

### Planned

| Feature | Description |
|---------|-------------|
| Web Search | DuckDuckGo / SerpAPI integration |
| Long-term Memory | SQLite-based persistent storage |
| Research Workflow | Multi-step research (search → gather → synthesize) |
| Error Handling | Timeouts, retries, graceful failures |

## Setup

```bash
cd /home/jwg/dev/research-agent

# Install dependencies
uv sync

# Start Ollama (if not running)
ollama serve

# Pull model (if not already)
ollama pull qwen3:1.7b
```

## Usage

```bash
uv run python main.py
```

Example interactions:
```
> What time is it now?
The current time is 2026-02-19 12:53:28.

> Write "Hello World" to /tmp/test.txt
Successfully wrote to /tmp/test.txt

> Read /tmp/test.txt
The content is: Hello World
```

## Configuration

Edit `config.py`:

```python
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen3:1.7b"
MAX_ITERATIONS = 10
```

## Adding New Tools

1. Create a new tool class inheriting from `Tool`:

```python
class MyTool(Tool):
    def __init__(self):
        super().__init__(
            name="my_tool",
            description="What this tool does",
            func=self._execute,
        )

    def _execute(self, param: str) -> str:
        return f"Result: {param}"
```

2. Add to `get_default_tools()` in `tools.py`

## Performance Notes

- qwen3:1.7b is lightweight but slower with tool calls (~20s)
- Consider qwen3:4b for faster responses
- Web search currently disabled (API unavailable)
