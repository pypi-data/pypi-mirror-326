# y-cli 🚀

A tiny command-line interface chat application that brings AI conversations to your terminal.

## ✨ Features

- 💬 Interactive chat interface
- 📝 All chat data stored in single JSONL files for easy access and sync
- 🔗 MCP (Model Context Protocol) client support
- 🤔 Deepseek-r1 reasoning content support for enhanced AI responses

## Demo

### MCP client
![mcp](.github/visuals/mcp.gif)

[asciicast](https://asciinema.org/a/702199)

### reasoning content
![r1](.github/visuals/r1.gif)

[asciicast](https://asciinema.org/a/702204)

## ⚡ Quick Start

### Prerequisites

Required:
1. uv
2. OpenRouter API key

Setup Instructions:
1. **uv**
   - Follow the [official installation guide](https://docs.astral.sh/uv/getting-started/installation/)
   - uv will automatically manage Python installation

2. **OpenRouter API key**
   - Visit [OpenRouter Settings](https://openrouter.ai/settings/keys)
   - Create a new API key
   - Save it for the initialization step

### Run without Installation
```bash
uvx y-cli
```

### Install with uv tool
```bash
uv tool install y-cli
```

### Initialize
```bash
y-cli init
```

### Start Chat
```bash
y-cli chat
```

## 🛠️ Usage

```bash
y-cli [OPTIONS] COMMAND [ARGS]...
```

### Commands
- `chat`   Start a new chat conversation or continue an existing one
- `list`   List chat conversations with optional filtering
- `share`  Share a chat conversation by generating a shareable link

### Options
- `--help`  Show help message and exit
