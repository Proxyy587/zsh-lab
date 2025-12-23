import json
import os
import requests
from typing import Any, Dict, List

CONFIG_DIR = os.path.expanduser("~/.config/zsh-lab")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

AVAILABLE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-4o",
    "gpt-4o-mini",
    "gpt-4.1"
]
DEFAULT_MODEL = "gpt-4o-mini"

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

def set_model(model: str) -> None:
    if model not in AVAILABLE_MODELS:
        print(f"Model '{model}' not recognized.\nRun 'gpt --list-models' to see available models.")
        return
    config = load_config()
    config["gpt_model"] = model
    save_config(config)
    print(f"Default model set to '{model}'.")

def get_current_model() -> str:
    config = load_config()
    model = config.get("gpt_model", DEFAULT_MODEL)
    if model not in AVAILABLE_MODELS:
        return DEFAULT_MODEL
    return model

def list_models() -> None:
    current_model = get_current_model()
    print("Available models:")
    for m in AVAILABLE_MODELS:
        marker = ""
        if m == current_model:
            marker = " (current default)"
        print(f"  {m}{marker}")

def query(prompt: str, model: str = None) -> None:
    config = load_config()
    token = config.get("gpt_token")
    if not token:
        print("Token not set. Please set it using: gpt --token YOUR_KEY")
        return

    if model is None:
        model = get_current_model()
    elif model not in AVAILABLE_MODELS:
        print(f"Model '{model}' not recognized. Run 'gpt --list-models' to see available models.")
        return

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    data: Dict[str, Any] = {
        "model": model,
        "input": prompt
    }

    url = "https://api.openai.com/v1/responses"
    try:
        res = requests.post(url, headers=headers, json=data, timeout=60)
        res.raise_for_status()
        payload = res.json()
        # Handle streamed or non-streamed as non-stream only now
        if payload.get('status') == 'error' or payload.get("error"):
            print("API Error:", payload.get("error") or payload)
            return
        # print output text only (output type is a list of dicts, type=='message', content=[ ... ])
        output = payload.get("output")
        if not output:
            print("No response from model.")
            return
        for o in output:
            if o["type"] == "message":
                for seg in o.get("content", []):
                    if seg["type"] == "output_text":
                        print(seg["text"])
        # optionally also print usage and reasoning
        if payload.get("reasoning"):
            print("\n[reasoning]:", json.dumps(payload["reasoning"], indent=2, ensure_ascii=False))
        if payload.get("usage"):
            print("\n[usage]:", payload["usage"])
    except requests.HTTPError as e:
        if e.response is not None and e.response.status_code == 429:
            print("Too Many Requests (429) - You have hit a rate limit. Please try again later.")
        else:
            print(f"Request error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def handle(args: list[str]) -> None:
    if not args:
        print("invalid command: gpt [--token <your_key> | --set-model <model> | --list-models | [--model <model>] <prompt>]")
        return

    model = None
    prompt_args = []
    idx = 0
    while idx < len(args):
        arg = args[idx]
        if arg == "--token":
            if idx + 1 >= len(args):
                print("invalid command: gpt --token <your_key>")
                return
            set_token(args[idx + 1])
            return
        elif arg in ("--list-models", "-l"):
            list_models()
            return
        elif arg in ("--set-model", "-s"):
            if idx + 1 >= len(args):
                print("invalid command: gpt --set-model <model>")
                return
            set_model(args[idx + 1])
            return
        elif arg == "--model":
            if idx + 1 >= len(args):
                print("invalid command: gpt --model <model> <prompt>")
                return
            model = args[idx + 1]
            idx += 2
        else:
            prompt_args.append(arg)
            idx += 1

    if not prompt_args:
        print("No prompt provided.")
        return

    prompt = " ".join(prompt_args)
    query(prompt, model)
