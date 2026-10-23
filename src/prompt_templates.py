from pathlib import Path
from string import Formatter


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
LANGUAGES = ("English", "German", "French", "Spanish")


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


def _load_banned_phrases():
    path = TEMPLATES_DIR / "banned_phrases.txt"
    try:
        phrases = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Banned phrase list not found: {path}") from error
    if not phrases:
        raise ValueError(f"Banned phrase list is empty: {path}")
    return ", ".join(phrases)


def build_prompts(channel, product, topic, brand_voice, product_facts,
                  past_posts="", secondary_context="", language="English"):
    # Keep one value for every template placeholder.
    values = {
        "channel": channel,
        "product": product,
        "topic": topic,
        "brand_voice": brand_voice,
        "product_facts": product_facts,
        "past_posts": past_posts,
        "secondary_context": secondary_context,
        "language": language,
        "banned_phrases": _load_banned_phrases(),
    }
    for name, value in values.items():
        if not isinstance(value, str):
            raise ValueError(f"{name} must be a string.")
        values[name] = value.strip()
        if not values[name] and name not in ("past_posts", "secondary_context"):
            raise ValueError(f"{name} must not be empty.")

    # Reject unsupported languages with the supported choices.
    if values["language"] not in LANGUAGES:
        raise ValueError(f"Unsupported language {values['language']!r}. Choose one of: {', '.join(LANGUAGES)}")

    # A channel is a filename stem, never a path supplied by the caller.
    channel = values["channel"]
    if not all(char.isascii() and (char.isalnum() or char in "_-") for char in channel) or channel == "system":
        raise ValueError("channel must be a template name such as 'linkedin' or 'email'.")

    values["past_posts"] = values["past_posts"] or "No past posts supplied."
    values["secondary_context"] = values["secondary_context"] or "No secondary context supplied."

    system_prompt = _fill_template(TEMPLATES_DIR / "system.txt", values)
    user_prompt = _fill_template(TEMPLATES_DIR / f"{channel}.txt", values)
    return system_prompt, user_prompt


def build_prompt(channel, product, topic, context, language="English"):
    # Adapt the knowledge-base context dictionary to build_prompts.
    return build_prompts(
        channel,
        product,
        topic,
        context["brand_voice"],
        context["product_facts"],
        context["past_posts"],
        context["secondary_context"],
        language=language,
    )


# Run this file directly to preview both prompts with real product context.
if __name__ == "__main__":
    from knowledge_base import choose_context, load_knowledge_base

    pieces = load_knowledge_base()
    context = choose_context(pieces, "gravel")
    system_prompt, user_prompt = build_prompt(
        "linkedin", "gravel", "autumn gravel season", context
    )
    print("=== SYSTEM PROMPT ===")
    print(system_prompt)
    print("=== USER PROMPT ===")
    print(user_prompt)
    print("PASS: Built both prompts using the real knowledge base.")
