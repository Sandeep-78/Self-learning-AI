# Self-Learning AI Agent 🤖

A beginner-friendly Python AI assistant that uses an LLM and persistent local memory. It can use saved facts in later conversations and stores a short log of recent interactions.

> **Note:** This is a learning project, not a model that retrains itself. Its memory improves continuity; it does not change the underlying model weights.

## Features
- Chat with an OpenAI model
- Persistent local memory stored in `memory.json`
- Explicitly save facts with `/remember <fact>`
- View saved facts with `/memory`
- Remove a saved fact with `/forget <number>`
- Keep a limited local record of recent interactions

## Requirements
- Python 3.10+
- An OpenAI API key with API access (API usage may incur charges)

## Setup (Windows)

1. Download or clone this repository and open the folder in a terminal.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env` and add your API key to `OPENAI_API_KEY`.
5. Run the agent:

   ```powershell
   python main.py
   ```

## Commands

- `/remember I prefer short answers` — save a fact to long-term memory
- `/memory` — list saved facts
- `/forget 1` — delete saved fact number 1
- `/quit` — exit

## Project structure

```text
self-learning-ai-agent/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Security
- Never commit your `.env` file or API key.
- `memory.json` may contain personal information, so it is excluded from Git.
- Only save information you actually want the agent to retain.

## Future improvements
- Add vector search using Qdrant
- Add Mem0 for more advanced memory management
- Add a web UI
- Add tools and feedback-based evaluation

## License
MIT
