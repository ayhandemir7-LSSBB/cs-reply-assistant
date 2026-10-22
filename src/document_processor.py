# Reads the markdown knowledge bases and cuts them into labelled pieces (M1, M2).
# It prepares the pieces. It doesn't choose them, and it doesn't call the LLM.

import re
from pathlib import Path
import mistune

# knowledge_base/ sits next to src/, so the path works from any folder
KB_DIR = Path(__file__).resolve().parent.parent / "knowledge_base"

# mistune with renderer=None returns the markdown as a list of tokens (headings, paragraphs, lists)
parse_markdown = mistune.create_markdown(renderer=None)


def token_to_text(token):
    # Turn one token (and everything inside it) back into plain text
    if token["type"] in ("softbreak", "linebreak"):
        return " "
    if token["type"] == "list":
        return "\n".join("- " + token_to_text(item) for item in token["children"])
    if "raw" in token:
        return token["raw"]
    return "".join(token_to_text(child) for child in token.get("children", []))


def load_markdown_file(path, source):
    # Read one .md file and split it into pieces at every ## heading
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        print(f"Skipped empty file: {path.name}")
        return []

    file_name = path.relative_to(KB_DIR / source).as_posix()

    # Date from the header line "Collected: YYYY-MM-DD" (empty if missing)
    date_match = re.search(r"Collected:\s*(\d{4}-\d{2}-\d{2})", text)
    date = date_match.group(1) if date_match else ""

    title = ""
    body = []      # all text after the # title (used for past posts)
    pieces = []    # one piece per ## heading
    for token in parse_markdown(text):
        if token["type"] == "blank_line":
            continue
        if token["type"] == "heading" and token["attrs"]["level"] == 1:
            title = token_to_text(token)
            continue
        body.append(token_to_text(token))
        if token["type"] == "heading" and token["attrs"]["level"] == 2:
            # A new ## heading starts a new piece
            pieces.append({"source": source, "file": file_name, "heading": token_to_text(token), "text": "", "date": date})
        elif pieces:
            # Everything under a heading belongs to that piece
            pieces[-1]["text"] += token_to_text(token) + "\n"

    # Past posts stay whole: one post = one piece, with or without ## headings
    if "past_content" in file_name:
        return [{"source": source, "file": file_name, "heading": title or path.stem, "text": "\n".join(body), "date": date}]

    if not pieces:
        print(f"No ## headings found, file not split: {source}/{file_name}")

    # Drop headings with no text under them
    return [p for p in pieces if p["text"].strip()]


def load_knowledge_base():
    # Find every .md file in primary/ and secondary/ and return all pieces in one list
    all_pieces = []
    for source in ("primary", "secondary"):
        folder = KB_DIR / source
        if not folder.exists():
            raise FileNotFoundError(f"Folder not found: {folder}")
        for path in sorted(folder.rglob("*.md")):
            all_pieces += load_markdown_file(path, source)
    return all_pieces


# Check for card 3.1: python src/document_processor.py
if __name__ == "__main__":
    pieces = load_knowledge_base()
    files = sorted({(p["source"], p["file"]) for p in pieces})

    print(f"Files with content: {len(files)}")
    for source, file in files:
        count = sum(1 for p in pieces if p["file"] == file and p["source"] == source)
        print(f"  {source}/{file}: {count} pieces")

    print(f"\nTotal pieces: {len(pieces)}")
    print("Every piece has a heading:", all(p["heading"] for p in pieces))

    print("\nExample piece:")
    print(pieces[0] if pieces else "No pieces found")
