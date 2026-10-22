# agents.md: CS Reply Assistant

## Purpose
A tool that gives customer service agents draft replies to customer messages, written in the company's voice and based only on the company's knowledge base. Demo client: Canyon Bicycles. Swapping the `knowledge_base/` files makes it work for any organisation. Musts M1–M8 are in `project_structure.md`, section 4.

## Stack & run
- Python 3.12
- Main command: `python src/main.py "customer message" email` (channel: `email` or `chat`)
- Install: `pip install -r requirements.txt`
- Env vars in `.env` (copy `.env.example`): `OPENAI_API_KEY`, `LLM_MODEL` (default `gpt-4o-mini`). Never commit `.env`.

## Repo map
- `knowledge_base/primary/`: company documents (brand voice, products, CS policies, example replies)
- `knowledge_base/secondary/`: industry context (market trends, competitors)
- `templates/`: prompt templates (`system.txt` rules + one file per channel)
- `src/document_processor.py`: reads and splits the markdown (M1, M2)
- `src/knowledge_base.py`: picks the KB pieces per request
- `src/prompt_templates.py`: fills the templates (M4)
- `src/llm_integration.py`: the only file that calls the OpenAI API (M3)
- `src/content_pipeline.py` + `src/main.py`: runs the steps end to end (M5)
- `outputs/`: saved replies

## Conventions
- One file = one job; keep functions short and simple, with `#` comments
- New prompt types go in `templates/` as a new `.txt` file, not in Python code
- Read settings from `.env` with `python-dotenv`; no hard-coded keys or model names
- Clear errors for missing files, missing key or API failure
- Commit messages say what changed, e.g. "add markdown loader"

## Definition of Done (agent changes)
- Matches Kanban DoD
- Code/docs for the card are in the repo
- The Must "How we verify" check passes
- Touches only the active card / Must ID
- No secrets committed

## Never do
- Commit `.env` or API keys
- Expand into the Won't list (RAG, auto-sending replies, CRM integration) without team agreement
- Invent APIs or KB facts (policies, prices, product details); use only the knowledge base
- Use real customer data (GDPR); test messages are invented
- Work directly on `main`

## How we use agents
- One Trello card at a time; paste the card title + Must ID into the prompt
- Point the agent at this file first: "Read agents.md, then do card 3.1 (M1)"
- Review the agent's changes before committing
