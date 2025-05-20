# AI Agent Playground

I'm just playing around with AI Agents! Specifically, the new [Python AI Agents SDK from OpenAI](https://github.com/openai/openai-agents-python). This project uses [uv](https://github.com/astral-sh/uv) as a python version manager

## Usage
Install dependencies
```sh
uv pip sync requirements.txt
```

Run the main program for a basic "ChatGPT" experience:
```sh
uv run main.py
```

Play a game of ~~Akinator~~ Err... Rotanika:
```sh
uv run akinator.py
```

Run a program that helps to iteratively develop a plot overview which can then be be converted into a screenplay
```sh
uv run plot_overview.py
```

## Development
In VSCode, by default, alt+z activates word wrap. There are a lot of long strings in the projects
