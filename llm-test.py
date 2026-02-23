import requests
import json
import time


OPENWEBUI_URL = "https://ai.datagaucho.com"
API_KEY = "sk-b3ce02f3eb5948f4b36a86c4ce23818e"
MODEL_NAME = "gpt-oss:latest"

def ask_openwebui(prompt, system_prompt=None, temperature=0.0):
    messages = []
    start_time = time.time()

    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })

    messages.append({
        "role": "user",
        "content": prompt
    })

    response = requests.post(
        f"{OPENWEBUI_URL}/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": temperature,
            "stream": True  ,
            "seed": 48,
            "top_p": 1.0,
            "top_k": 1.0,
            "repeat_penalty": 1.0,
            "mirostat": 0,
        },
        stream=True,
        timeout=200
    )

    full_response = ""

    for line in response.iter_lines():
        if not line:
            continue

        decoded = line.decode("utf-8")

        if not decoded.startswith("data: "):
            continue

        chunk = decoded.replace("data: ", "")

        if chunk == "[DONE]":
            break

        try:
            chunk_json = json.loads(chunk)
        except json.JSONDecodeError:
            continue

        if "choices" not in chunk_json:
            continue

        choice = chunk_json["choices"][0]
        delta = choice.get("delta", {})

        if "content" in delta:
            token = delta["content"]
            print(token, end="", flush=True)
            full_response += token


    print()  # newline after streaming
    print("\nDone in", round(time.time() - start_time, 2), "seconds")

    return full_response

print(
    ask_openwebui(
        "Explain what a DISARM tactic is in one sentence.",
        system_prompt="You are a cybersecurity analyst."
    )
)