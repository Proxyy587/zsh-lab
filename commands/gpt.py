import json
import os
from typing import Any, Dict, List

import requests


CONFIG_DIR = os.path.expanduser("~/.config/zsh-lab")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

def _ensure_config_dir() -> None:
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config() -> Dict[str, Any]:
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(data: Dict[str, Any]) -> None:
    _ensure_config_dir()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def set_token(token: str) -> None:
    config = load_config()
    config["gpt_token"] = token
    save_config(config)
    print("GPT token saved.")


def query(prompt: str) -> None:
    config = load_config()
    token = config.get("gpt_token")

    if not token:
        print("Token not set. Please set it using: gpt --token YOUR_KEY")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {
        # TODO: Make this configurable
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt},
        ],
    }

    try:
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )
        res.raise_for_status()
        payload = res.json()
        choices: List[Dict[str, Any]] = payload.get("choices", [])
        if not choices:
            print("No response from model.")
            return
        print(choices[0]["message"]["content"])
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def handle(args: list[str]) -> None:
    # gpt --token YOUR_KEY | gpt "prompt"
    if not args:
        print("invalid command: gpt [--token <your_key> | <prompt>]")
        return

    if args[0] == "--token":
        if len(args) < 2:
            print("invalid command: gpt --token <your_key>")
            return
        set_token(args[1])
        return

    prompt = " ".join(args)
    query(prompt)
