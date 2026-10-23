from pathlib import Path
import sys

from content_pipeline import run_in_terminal
from knowledge_base import PRODUCTS
from prompt_templates import LANGUAGES


TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"


def _allowed_channels():
    # Only channel templates are valid; shared prompt files are excluded.
    return sorted(
        path.stem for path in TEMPLATES_DIR.glob("*.txt")
        if path.stem not in ("system", "banned_phrases")
    )


def _usage(program, channels):
    print(f'Usage: {program} <channel> <product> "<topic>" [language]')
    print("Channels: " + ", ".join(channels))
    print("Products: " + ", ".join(PRODUCTS))
    print("Languages: " + ", ".join(LANGUAGES))
    print('Example: python src/main.py linkedin gravel "autumn gravel season" German')


def main(args=None):
    # Check every argument before entering the pipeline.
    if args is None:
        args = sys.argv[1:]
    channels = _allowed_channels()
    if len(args) not in (3, 4):
        _usage("python src/main.py", channels)
        return 1

    requested_channel, requested_product, topic = args[:3]
    requested_language = args[3] if len(args) == 4 else "English"
    channel = requested_channel.casefold()
    product_key = requested_product.casefold()
    language_key = requested_language.casefold()
    products_by_key = {product.casefold(): product for product in PRODUCTS}
    languages_by_key = {language.casefold(): language for language in LANGUAGES}
    errors = []

    if channel not in channels:
        errors.append(f"Invalid channel: {requested_channel}")
    if product_key not in products_by_key:
        errors.append(f"Invalid product: {requested_product}")
    if language_key not in languages_by_key:
        errors.append(f"Invalid language: {requested_language}")
    if not topic.strip():
        errors.append("Topic must not be empty")
    if errors:
        for error in errors:
            print(error)
        _usage("python src/main.py", channels)
        return 1

    saved_path = run_in_terminal(
        channel,
        products_by_key[product_key],
        topic.strip(),
        languages_by_key[language_key],
    )
    return 0 if saved_path else 1


if __name__ == "__main__":
    raise SystemExit(main())
