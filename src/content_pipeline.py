from datetime import datetime
from pathlib import Path
import re

from document_processor import load_knowledge_base
from knowledge_base import choose_context
from llm_integration import MODEL, call_llm
from prompt_templates import build_prompt


LANGUAGE_CODES = {
    "English": "en",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
}
OUTPUTS_DIR = Path(__file__).resolve().parent.parent / "outputs"
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _count_emoji(text):
    # Count emoji bases, paired flags, and joined emoji sequences.
    def is_emoji_base(codepoint):
        return 0x1F000 <= codepoint <= 0x1FAFF or 0x2600 <= codepoint <= 0x27BF

    count = 0
    index = 0
    while index < len(text):
        codepoint = ord(text[index])
        if 0x1F1E6 <= codepoint <= 0x1F1FF:
            count += 1
            index += 1
            if index < len(text) and 0x1F1E6 <= ord(text[index]) <= 0x1F1FF:
                index += 1
            continue
        if not is_emoji_base(codepoint):
            index += 1
            continue
        count += 1
        index += 1
        while index < len(text) and (0xFE00 <= ord(text[index]) <= 0xFE0F or 0x1F3FB <= ord(text[index]) <= 0x1F3FF):
            index += 1
        while index + 1 < len(text) and ord(text[index]) == 0x200D and is_emoji_base(ord(text[index + 1])):
            index += 2
            while index < len(text) and (0xFE00 <= ord(text[index]) <= 0xFE0F or 0x1F3FB <= ord(text[index]) <= 0x1F3FF):
                index += 1
    return count


def generate_draft(channel, product, topic, language="English", feedback=""):
    # Build context and prompts, then request one draft.
    pieces = load_knowledge_base()
    context = choose_context(pieces, product)
    system_prompt, user_prompt = build_prompt(channel, product, topic, context, language)
    if feedback.strip():
        user_prompt += f"\n\nRevise the draft with this feedback: {feedback.strip()}"
    return call_llm(user_prompt, system_prompt)


def check_quality(draft, channel):
    # Read the shared banned list and measure output formatting.
    path = TEMPLATES_DIR / "banned_phrases.txt"
    try:
        banned_phrases = [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except FileNotFoundError as error:
        raise FileNotFoundError(f"Banned phrase list not found: {path}") from error
    lowered = draft.casefold()
    banned_found = [phrase for phrase in banned_phrases if phrase.casefold() in lowered]
    em_dashes = draft.count("—")
    # Count heading markers, not permitted LinkedIn hashtags; hashtags are checked separately.
    markdown_symbols = len(re.findall(r"(?m)^\s{0,3}#{1,6}\s+", draft)) + draft.count("**") + draft.count("__")
    emoji_count = _count_emoji(draft)
    hashtag_count = len(re.findall(r"(?<!\w)#[\w]+", draft))
    word_count = len(re.findall(r"\b[\w]+(?:['’][\w]+)*\b", draft, flags=re.UNICODE))
    lower, upper = (120, 200) if channel == "linkedin" else (120, 180) if channel == "email" else (0, float("inf"))
    word_count_ok = lower <= word_count <= upper
    return {
        "banned_phrases_found": banned_found,
        "em_dashes": em_dashes,
        "markdown_symbols": markdown_symbols,
        "emoji_count": emoji_count,
        "hashtag_count": hashtag_count,
        "word_count": word_count,
        "word_count_ok": word_count_ok,
        "ok": not banned_found and em_dashes == 0 and markdown_symbols == 0 and emoji_count <= 2 and hashtag_count <= 3 and word_count_ok,
    }


def save_post(draft, channel, product, topic, language, quality):
    # Save one approved draft with its quality summary.
    if language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported language {language!r}. Choose one of: {', '.join(LANGUAGE_CODES)}")
    created = datetime.now()
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{channel}_{product}_{LANGUAGE_CODES[language]}_{created:%Y%m%d-%H%M%S}.md"
    output_path = OUTPUTS_DIR / filename
    banned = ", ".join(quality.get("banned_phrases_found", [])) or "none"
    header = (
        "---\n"
        f"channel: {channel}\n"
        f"product: {product}\n"
        f"topic: {topic}\n"
        f"language: {language}\n"
        f"model: {MODEL}\n"
        f"created: {created:%Y-%m-%d %H:%M:%S}\n"
        f"quality_ok: {str(bool(quality.get('ok', False))).lower()}\n"
        f"banned_phrases_found: {banned}\n"
        "---\n\n"
    )
    output_path.write_text(header + draft.rstrip() + "\n", encoding="utf-8")
    return str(output_path)


def run_in_terminal(channel, product, topic, language="English"):
    # Let the user revise until they approve a draft.
    feedback = ""
    while True:
        try:
            draft = generate_draft(channel, product, topic, language, feedback)
            quality = check_quality(draft, channel)
            print(draft)
            if quality["ok"]:
                print("Quality check: PASS")
            else:
                warnings = []
                if quality["banned_phrases_found"]:
                    warnings.append("banned phrases")
                if quality["em_dashes"]:
                    warnings.append("em dashes")
                if quality["markdown_symbols"]:
                    warnings.append("Markdown symbols")
                if quality["emoji_count"] > 2:
                    warnings.append("too many emojis")
                if quality["hashtag_count"] > 3:
                    warnings.append("too many hashtags")
                if not quality["word_count_ok"]:
                    warnings.append("word count")
                print("Quality warnings: " + ", ".join(warnings))
            feedback = input("Press Enter to approve and save, or type feedback: ").strip()
            if not feedback:
                output_path = save_post(draft, channel, product, topic, language, quality)
                print(f"Saved approved draft: {output_path}")
                return output_path
        except (ValueError, ConnectionError) as error:
            print(str(error))
            return None
