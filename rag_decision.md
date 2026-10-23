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


# RAG Decision: Rule-Based Selection and Direct Context Injection

**Project:** AI Content Creator — Canyon Bicycles  
**Review date:** 23 October 2026  
**Status:** Proposed for team review and approval

## 1. Decision

For the current project scope, we use **explicit rules to select product information and inject context directly into the prompts**. We do not currently use embeddings, semantic search, or a vector database.

This is a scope-based engineering decision, not a claim that RAG is generally unnecessary or that direct injection guarantees accurate output.

RAG can use lexical, metadata-based, semantic, or hybrid retrieval; it does not necessarily require a vector database. The precise description of our current approach is **rule-based context selection and direct injection, without a search index**.

## 2. Current implementation

The application supports four channels—LinkedIn, email, Instagram, and newsletter—three product families—gravel, road, and mountain—and four output languages: English, German, French, and Spanish. The user also provides a free-text topic.

The pipeline:

1. `src/document_processor.py` reads the Markdown knowledge bases and splits ordinary documents at `##` headings. Files in `past_content/` remain whole.
2. `src/knowledge_base.py` selects product-specification sections whose headings start with the chosen family.
3. It also includes all brand guidelines, all past-content examples, and all secondary knowledge-base sections.
4. `src/prompt_templates.py` inserts the context into the shared system template and the channel template.
5. The model generates a draft, followed by partial formatting checks and human review before approval and saving through the interface.

Context selection currently depends on the product family, not on the topic, channel, or language. Each generation makes one model call; each rewrite makes another.

## 3. Seven reasons for the decision

| Criterion | Project-specific justification | Boundary of the argument |
|---|---|---|
| **1. The product family is already known** | The user explicitly chooses one of three families. Rules can select its specification sections without inferring relevance through semantic similarity. | A family label does not resolve every topic or distinguish every model version. |
| **2. Selected specifications can be included in full** | Including the recognized sections avoids depending on a search ranking to return each condition or specification within those sections. | Receiving the text does not guarantee that the model preserves or interprets every condition correctly. |
| **3. Selection is inspectable** | The team can inspect the filenames and headings used by the selector and explain why a specification section was included. | Rules remain dependent on consistent document structure and require review when that structure changes. |
| **4. Complexity should match the scope** | Semantic retrieval would add decisions about embeddings, indexing, updates, filters, result counts, and retrieval evaluation. We have not demonstrated a benefit that justifies this additional work for the current workflow. | This does not establish that retrieval would take a fixed amount of time or could never improve results. |
| **5. Document updates are available directly** | The pipeline reads the Markdown files on each generation, so edits become available without a separate reindexing step. | The documents still need editorial checks for accuracy and freshness. |
| **6. There is no separate index to synchronize** | Direct reading avoids an additional failure mode in which the source document changes but a search index still contains an earlier version. | It does not provide version history or full traceability of previously generated drafts. |
| **7. More immediate improvements are available** | Better source quality, more precise secondary-context filtering, and stronger output checks address observed weaknesses before adding a search component. | These improvements are proposals and must be evaluated; their benefits have not yet been measured. |

The corpus contains seven Markdown files and approximately 11,200 whitespace-separated words. The two secondary documents account for about 72% of those words. Stored comparison prompts contain roughly 73,000 characters in the system message alone. These are not token counts.

Therefore, the justification is **not** that the entire corpus is tiny. It is that product selection is structured and the team can first evaluate simpler, more precise filtering of the secondary material.

We avoid embedding calls and vector-index operation, but we have not measured total cost or latency against an alternative. Longer prompts and repeated rewrites must also be considered.

## 4. Limitations and required review

Only the specification block is filtered by family. Brand guidelines, past examples, and secondary documents contain other products and categories. Prompt instructions restrict their use, but do not guarantee that the model will never mix information.

The product material also combines published specifications, interpreted benefits, and editorial ideas. These should not be treated as equally strong evidence. Range-level features must not automatically be attributed to every model or version.

The secondary documents describe an “All + selected category” filter that the current selector does not implement. The team should align the documentation and behavior. The three past-content examples also repeat essentially the same body and need review.

Automatic checks cover selected formatting and house-style rules, not factual accuracy or full template compliance. The production checker currently does not enforce Instagram or newsletter word-count bounds. Human review must check product identity, figures, qualifications, and attribution.

**Adding RAG would not, by itself, fix duplicated examples, ambiguous source material, or incomplete output validation.** Those require document and validation improvements regardless of the retrieval strategy.

## 5. What the existing comparison supports

The five paired examples in `uniqueness/` compare the project pipeline with the same declared API model without company documents. They provide illustrative evidence of more specific, KB-traceable content in several cases, while retaining factual-qualification, length, and style weaknesses.

The comparison evaluates the combined context-and-instruction package. It does not compare injection with RAG, isolate the contribution of each component, verify external product truth, or establish general superiority. It is not a test of the ChatGPT application.

## 6. When to revisit

Reassess the decision if:

- The catalogue grows substantially across models and versions.
- Necessary information becomes spread across long documents.
- Requests become open-ended questions rather than content for a selected family.
- Rules repeatedly omit necessary information or include excessive irrelevant context.
- Different markets or languages require different authoritative sources.
- Measured token usage, latency, cost, or review effort exceeds agreed targets.
- A controlled evaluation demonstrates an advantage from retrieval.

Possible next steps include category filtering, lexical search, metadata-based retrieval, or a hybrid approach. A vector database is not the automatic next step. Adding output languages alone does not require RAG.

## 7. Conclusion

We retain rule-based selection and direct injection because they fit the current structured product workflow and avoid introducing components whose benefit has not yet been demonstrated.

The decision is provisional and evidence-based: prioritize source quality, context relevance, and validation, then introduce more advanced retrieval if evaluation shows that it solves a material need.


