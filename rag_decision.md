# rag_decision.md: Inject or Retrieve?



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


