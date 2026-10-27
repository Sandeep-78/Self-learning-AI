"""A small self-learning-style AI assistant with persistent local memory.

It stores user-approved facts and conversation summaries in memory.json.
Requires an OpenAI API key in .env.
"""
import json
import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "memory.json"
load_dotenv(BASE_DIR / ".env")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
API_KEY = os.getenv("OPENAI_API_KEY")


def load_memory():
    if not MEMORY_FILE.exists():
        return {"facts": [], "recent_conversations": []}
    try:
        return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"facts": [], "recent_conversations": []}


def save_memory(memory):
    MEMORY_FILE.write_text(json.dumps(memory, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    if not API_KEY:
        print("Missing OPENAI_API_KEY. Copy .env.example to .env and add your API key.")
        return

    client = OpenAI(api_key=API_KEY)
    memory = load_memory()
    history = []
    print("\nSelf-Learning AI Agent")
    print("Commands: /remember <fact>, /memory, /forget <number>, /quit\n")

    while True:
        try:
            user_text = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not user_text:
            continue
        if user_text.lower() in {"/quit", "quit", "exit"}:
            break
        if user_text == "/memory":
            print("\nSaved facts:")
            if not memory["facts"]:
                print("  (none yet)")
            for i, fact in enumerate(memory["facts"], 1):
                print(f"  {i}. {fact}")
            print()
            continue
        if user_text.startswith("/remember "):
            fact = user_text[len("/remember "):].strip()
            if fact and fact not in memory["facts"]:
                memory["facts"].append(fact)
                save_memory(memory)
                print("Agent: Saved that fact to long-term memory.\n")
            else:
                print("Agent: That fact is empty or already saved.\n")
            continue
        if user_text.startswith("/forget "):
            try:
                index = int(user_text[len("/forget "):]) - 1
                removed = memory["facts"].pop(index)
                save_memory(memory)
                print(f"Agent: Removed: {removed}\n")
            except (ValueError, IndexError):
                print("Agent: Use /forget followed by a valid fact number.\n")
            continue

        facts = "\n".join(f"- {fact}" for fact in memory["facts"]) or "(no saved facts yet)"
        system_prompt = (
            "You are a helpful AI assistant with persistent memory. Use the saved facts when relevant. "
            "Do not claim you learned or saved a personal fact unless the user explicitly uses /remember. "
            "Be honest about uncertainty and concise.\n\nSaved user facts:\n" + facts
        )
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "system", "content": system_prompt}, *history[-10:], {"role": "user", "content": user_text}],
                temperature=0.7,
            )
            answer = response.choices[0].message.content or "I couldn't generate a response."
            print(f"Agent: {answer}\n")
            history.extend([{"role": "user", "content": user_text}, {"role": "assistant", "content": answer}])
            memory["recent_conversations"].append({"user": user_text, "assistant": answer})
            memory["recent_conversations"] = memory["recent_conversations"][-20:]
            save_memory(memory)
        except Exception as exc:
            print(f"Agent: API request failed: {exc}\n")


if __name__ == "__main__":
    main()
