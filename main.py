import json
import sys
import requests
import os

def load_config(path):
    with open(path, "r") as f:
        return json.load(f)

def load_character(path):
    with open(path, "r") as f:
        return json.load(f)

def load_history(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_history(path, messages):
    with open(path, "w") as f:
        json.dump(messages, f, indent=2)

def chat(prompt, history, config, character):
    system_prompt = character.get("personality", "cheerful anime girl who calls the user 'senpai'")
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": prompt})

    url = config["base_url"]
    headers = {"Content-Type": "application/json"}
    if "api_key" in config:
        headers["Authorization"] = f"Bearer {config['api_key']}"

    payload = {
        "model": config["model"],
        "messages": messages,
        "max_tokens": config.get("max_tokens", 1024),
        "temperature": config.get("temperature", 0.7)
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def main():
    character_path = sys.argv[1] if len(sys.argv) > 1 else "character.json"
    config_path = sys.argv[2] if len(sys.argv) > 2 else "config.json"

    config = load_config(config_path)
    character = load_character(character_path)
    name = character.get("name", "Yuki")

    hist_path = f"{character_path.split('/')[-1].replace('.json','')}_history.json"
    history = load_history(hist_path)

    for message in history:
        if message.get("role") == "user":
            print(f"\nYou: {message.get('content')}")
        elif message.get("role") == "assistant":
            print(f"\n{name}: {message.get('content')}")

    while True:
        try:
            user = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in ("/quit", "/exit", "/leave"):
            break
        if user.lower() in ("/flush", "/forget"):
            os.remove(hist_path)
            history = []
            continue
        if user.lower() in ("/cls", "/clear"):
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        if not user:
            continue

        try:
            reply = chat(user, history, config, character)
        except Exception as e:
            print(f"\nError: {e}")
            continue

        history.append({"role": "user", "content": user})
        history.append({"role": "assistant", "content": reply})
        save_history(hist_path, history)
        print(f"\n{name}: {reply}")

if __name__ == "__main__":
    main()