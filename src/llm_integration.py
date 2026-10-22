# Sends the prompt to OpenAI and brings back the draft reply.
# The only file in the project that talks to the LLM API (M3).

import os
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, NotFoundError, APIConnectionError

# Read the API key and model name from .env (never hard-code them)
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


def call_llm(user_prompt, system_prompt="You are a helpful assistant.", temperature=0.7):
    # Stop early with a clear message if the key is missing
    if not API_KEY:
        raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

    client = OpenAI(api_key=API_KEY)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()

    # Clear errors for the three things that usually fail
    except AuthenticationError:
        raise ValueError("The API key is wrong. Check OPENAI_API_KEY in your .env file.")
    except NotFoundError:
        raise ValueError(f"Model '{MODEL}' not found. Check LLM_MODEL in your .env file.")
    except APIConnectionError:
        raise ConnectionError("Could not reach OpenAI. Check your internet connection.")


# Hello-world test: python src/llm_integration.py
if __name__ == "__main__":
    print(f"Model: {MODEL}")
    print(call_llm("Say 'Hello from the CS Reply Assistant! How can I assist you to support our End Customers Today?' and nothing else."))
