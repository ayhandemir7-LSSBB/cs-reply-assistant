# Picks the knowledge base pieces each request needs, and keeps primary and secondary apart.
# How it chooses is our RAG decision: simple rules, no search by meaning (see rag_decision.md).

from document_processor import load_knowledge_base

PRODUCTS = ("gravel", "road", "mountain")


def pieces_to_text(pieces):
    # Join pieces into one text block, each with its heading
    return "\n\n".join(f"### {p['heading']}\n{p['text'].strip()}" for p in pieces)


def choose_context(pieces, product):
    # Rule 0: only the three product families we support
    product = product.lower()
    if product not in PRODUCTS:
        raise ValueError(f"Unknown product '{product}'. Choose one of: {', '.join(PRODUCTS)}")

    # Rule 4: skip empty pieces
    pieces = [p for p in pieces if p["text"].strip()]

    # Rule 1: always keep the brand voice
    brand_voice = [p for p in pieces if p["file"] == "brand_guidelines.md"]

    # Rule 2: only the product pieces whose heading starts with the chosen family ("Gravel: ...")
    product_facts = [p for p in pieces
                     if p["file"] == "product_specs.md"
                     and p["heading"].lower().startswith(product)]

    # Our addition: all past posts as tone examples
    past_posts = [p for p in pieces if p["file"].startswith("past_content/")]

    # Rule 3: the secondary KB is small, so take all of it
    secondary = [p for p in pieces if p["source"] == "secondary"]

    # Without product facts the LLM would invent them, so stop here
    if not product_facts:
        raise ValueError(f"No facts for '{product}' in product_specs.md. Headings must start with '{product.capitalize()}:'")

    # One text block per template placeholder (agreed with card 4.2)
    return {
        "brand_voice": pieces_to_text(brand_voice),
        "product_facts": pieces_to_text(product_facts),
        "past_posts": pieces_to_text(past_posts),
        "secondary_context": pieces_to_text(secondary),
    }


# Check for card 3.2: python src/knowledge_base.py
if __name__ == "__main__":
    all_pieces = load_knowledge_base()
    print(f"Loaded pieces: {len(all_pieces)}\n")

    # The 3 test requests: one per product family
    for product in PRODUCTS:
        context = choose_context(all_pieces, product)
        print(f"=== {product.upper()} ===")
        for block, text in context.items():
            headings = [line[4:] for line in text.splitlines() if line.startswith("### ")]
            print(f"  {block}: {len(headings)} pieces {headings}")
        print("  No empty blocks:", all(text.strip() for text in context.values()))
        print()
