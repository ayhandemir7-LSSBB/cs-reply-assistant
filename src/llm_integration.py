"""Sends the prompt to OpenAI and brings back the draft content.

The only file in the project that talks to the LLM API (M3).
"""

import os
import json
from urllib.error import HTTPError, URLError
from pathlib import Path
from urllib.request import Request, urlopen
from dotenv import load_dotenv

# Read the API key and model name from .env (never hard-code them)
env_file = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_file)

# .strip() removes stray spaces, newlines and quotes that sneak into env vars
API_KEY = (os.getenv("OPENAI_API_KEY") or "").strip().strip('"').strip("'")
MODEL = (os.getenv("LLM_MODEL") or "gpt-4o-mini").strip().strip('"').strip("'")

# Reasoning models (o1, o3, o4-mini, gpt-5, ...) reject a custom temperature
REASONING_PREFIXES = ("o1", "o3", "o4", "gpt-5")


def _supports_temperature(model):
    return not model.lower().startswith(REASONING_PREFIXES)


def call_llm(user_prompt, system_prompt="You are a helpful assistant.", temperature=0.7):
    # Stop early with a clear message if the key is missing
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if _supports_temperature(MODEL):
        payload["temperature"] = temperature

    try:
        request = Request(
            "https://api.openai.com/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))
        return result["choices"][0]["message"]["content"].strip()

    # Clear errors for the things that usually fail
    except HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        # Log OpenAI's own explanation so it shows up in the Render logs
        print(f"OpenAI error {error.code} (model={MODEL!r}): {body}", flush=True)

        try:
            message = json.loads(body)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            message = body

        if error.code in (401, 403):
            raise ValueError("The API key is wrong. Check OPENAI_API_KEY in your .env file.") from error
        if error.code == 404:
            raise ValueError(f"Model '{MODEL}' not found. Check LLM_MODEL in your .env file.") from error
        if error.code == 429:
            raise ValueError(f"Rate limit or quota reached: {message}") from error
        raise ValueError(f"OpenAI rejected the request ({error.code}): {message}") from error
    except URLError as error:
        raise ConnectionError("Could not reach OpenAI. Check your internet connection.") from error


# Hello-world test: python src/llm_integration.py
if __name__ == "__main__":
    print(f"Model: {MODEL!r}")
    print(call_llm("Say 'Hello from the Canyon Bikes AI Content Creator!' and nothing else."))