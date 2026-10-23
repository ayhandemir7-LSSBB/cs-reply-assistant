from pathlib import Path
from string import Formatter


# Resolve files from this module, regardless of where Python is started.
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _fill_template(path, values):
    # Check template fields before inserting KB text (which may contain braces).
    try:
        template = path.read_text(encoding="utf-8")
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Prompt template not found: {path}") from error

    try:
        for _, field, format_spec, conversion in Formatter().parse(template):
            if field is None:
                continue
            if field not in values or format_spec or conversion:
                raise ValueError(f"Unsupported placeholder {{{field}}} in {path.name}")
        return template.format(**values)
    except ValueError as error:
        raise ValueError(f"Cannot fill {path.name}: {error}") from error


def build_prompts(channel, product, topic, brand_voice, product_facts,
                  past_posts="", secondary_context=""):
    # These seven names are the shared interface with the context selector.
    values = {
        "channel": channel,
        "product": product,
        "topic": topic,
        "brand_voice": brand_voice,
        "product_facts": product_facts,
        "past_posts": past_posts,
        "secondary_context": secondary_context,
    }
    for name, value in values.items():
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string.")
        values[name] = value.strip()
        if not values[name] and name not in ("past_posts", "secondary_context"):
            raise ValueError(f"{name} must not be empty.")

    # A channel is a filename stem, never a path supplied by the caller.
    channel = values["channel"]
    if not all(char.isascii() and (char.isalnum() or char in "_-") for char in channel) or channel == "system":
        raise ValueError("channel must be a template name such as 'linkedin' or 'email'.")

    values["past_posts"] = values["past_posts"] or "No past posts supplied."
    values["secondary_context"] = values["secondary_context"] or "No secondary context supplied."

    system_prompt = _fill_template(TEMPLATES_DIR / "system.txt", values)
    user_prompt = _fill_template(TEMPLATES_DIR / f"{channel}.txt", values)
    return system_prompt, user_prompt


# Run this file directly to preview both templates without calling the AI.
# This block does not run when the pipeline imports build_prompts.
if __name__ == "__main__":
    # Deliberate sample labels: these are not real company or product facts.
    sample_inputs = {
        "product": "gravel",
        "topic": "autumn gravel rides",
        "brand_voice": "[Sample brand guidelines go here.]",
        "product_facts": "[Sample product facts go here.]",
        "past_posts": "[Sample past posts go here.]",
        "secondary_context": "[Sample industry context goes here.]",
    }

    for channel in ("linkedin", "email"):
        system_prompt, user_prompt = build_prompts(channel=channel, **sample_inputs)

        # Check that none of the seven template placeholders remain.
        for name in ("channel", *sample_inputs):
            placeholder = "{" + name + "}"
            if placeholder in system_prompt or placeholder in user_prompt:
                raise AssertionError(f"Unfilled placeholder: {placeholder}")

        print(f"\n=== {channel.upper()}: SYSTEM PROMPT ===")
        print(system_prompt)
        print(f"\n=== {channel.upper()}: USER PROMPT ===")
        print(user_prompt)
        print(f"\nPASS: {channel} template filled successfully.")
