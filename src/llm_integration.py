# Sends the prompt to OpenAI and brings back the draft content.
# The only file in the project that talks to the LLM API (M3).

import os
import json
from urllib.error import HTTPError, URLError
from pathlib import Path
from urllib.request import Request, urlopen

# Read the API key and model name from .env (never hard-code them)
env_file = Path(__file__).resolve().parent.parent / ".env"
if env_file.is_file():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            if key.startswith("export "):
                key = key[7:].strip()
            value = value.strip().strip("\"'")
            os.environ.setdefault(key, value)

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def call_llm(user_prompt, system_prompt="You are a helpful assistant.", temperature=0.7):
    # Stop early with a clear message if the key is missing
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    try:
        request = Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps({
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": temperature,
            }).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(request) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"].strip()

    # Clear errors for the three things that usually fail
    except HTTPError as error:
        if error.code in (401, 403):
            raise ValueError("The API key is wrong. Check OPENAI_API_KEY in your .env file.") from error
        if error.code == 404:
            raise ValueError(f"Model '{MODEL}' not found. Check LLM_MODEL in your .env file.") from error
        raise
    except URLError as error:
        raise ConnectionError("Could not reach OpenAI. Check your internet connection.") from error


# Hello-world test: python src/llm_integration.py
if __name__ == "__main__":
    print(f"Model: {MODEL}")
    print(call_llm("Say 'Hello from the Canyon Bikes AI Content Creator!' and nothing else."))
