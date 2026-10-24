# Sends the prompt to OpenAI and brings back the draft content.
# The only file in the project that talks to the LLM API (M3).

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI, APIStatusError, APIConnectionError

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

    request_options = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    }
    if _supports_temperature(MODEL):
        request_options["temperature"] = temperature

    try:
        client = OpenAI(api_key=API_KEY)
        response = client.chat.completions.create(**request_options)
        return response.choices[0].message.content.strip()

    # Keep the existing messages while translating SDK errors
    except APIStatusError as error:
        body = error.response.text
        print(f"OpenAI error {error.status_code} (model={MODEL!r}): {body}", flush=True)

        try:
            message = json.loads(body)["error"]["message"]
        except (ValueError, KeyError, TypeError):
            message = body

        if error.status_code in (401, 403):
            raise ValueError("The API key is wrong. Check OPENAI_API_KEY in your .env file.") from error
        if error.status_code == 404:
            raise ValueError(f"Model '{MODEL}' not found. Check LLM_MODEL in your .env file.") from error
        if error.status_code == 429:
            raise ValueError(f"Rate limit or quota reached: {message}") from error
        raise ValueError(f"OpenAI rejected the request ({error.status_code}): {message}") from error
    except APIConnectionError as error:
        raise ConnectionError("Could not reach OpenAI. Check your internet connection.") from error


# Hello-world test: python src/llm_integration.py
if __name__ == "__main__":
    print(f"Model: {MODEL!r}")
    print(call_llm("Say 'Hello from the Canyon Bikes AI Content Creator!' and nothing else."))
