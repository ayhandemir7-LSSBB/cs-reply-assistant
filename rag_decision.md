# rag_decision.md: Inject or Retrieve?

## Decision
**Inject (no RAG).** We load the markdown knowledge base, pick the pieces each request needs with simple rules (`src/knowledge_base.py`), and put them directly into the prompt. No chunk embeddings, no vector database, no search by meaning.

## Why: 5 criteria

| # | Criterion | Our situation | Points to |
|---|---|---|---|
| 1 | Corpus size & structure | About 6 short markdown files (brand voice, product specs for 3 families, past posts, market trends, competitor marketing), a few thousand words in total. Every file is split at `##` headings into labelled pieces (`src/document_processor.py`). Everything would fit in the prompt, but we still select: the chooser sends only the chosen product's pieces, so the model never mixes up gravel, road and mountain facts | Inject, with rule-based selection |
| 2 | How often does it change? | Rarely: only when Canyon updates a bike model or its brand guidelines; a team member edits the markdown file by hand | Inject |
| 3 | How different are the requests? | Narrow and structured: 2 channels × 3 products × one topic. The product choice tells us exactly which pieces are needed, so a rule finds them with certainty; semantic search could miss or mix products | Inject |
| 4 | Context window, cost, latency | Tradeoff: stuffing gets expensive and slow when the context is large; retrieval keeps prompts short but adds embedding calls, a vector store and the risk of missing a needed fact. Our selected context is small and fits easily in gpt-4o-mini's window, so stuffing costs little: one LLM call per request, no embedding calls, no store to host, and lower latency | Inject |
| 5 | Complexity vs 2-day scope | A RAG stack (chunking, embeddings, vector DB, retrieval tuning) would take most of a day and add failure points without improving the posts. The simpler approach that still delivers brand-aware uniqueness: (1) brand voice is always in the prompt, (2) only the chosen product's real facts, (3) past posts as tone examples, (4) one template per channel with the rule "use only these facts" (`templates/`), (5) human review before saving. The uniqueness comparison (`uniqueness/comparison.md`) shows the effect | Inject |

## How the choice serves the stakeholders
The marketing lead's quality need is that every post uses Canyon's real product facts and never invents one. Injecting guarantees the model always sees the brand voice and the complete facts for the chosen product; retrieval could leave out a fact the post needs. This is the context strategy behind Musts M1 to M3 (see `project_structure.md` §7).

## Revisit when
- The knowledge base grows to the full catalogue (dozens of models), multiple languages or long technical manuals
- Requests become open questions instead of a product choice (e.g. "which bike is best for bikepacking in the Alps?")
- The prompt gets too long or too expensive per request
