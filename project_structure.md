# project_structure.md: AI Content Creator

## 1. Project identity

| Item | Answer |
|---|---|
| Project name | AI Content Creator (demo client: Canyon Bicycles) |
| Primary project type | Organizational (reusable for any company by replacing the knowledge base files) |
| Defined goal | Give Canyon's marketing team LinkedIn posts and emails about its gravel, road and mountain bikes, written in Canyon's voice from Canyon's real product facts, and prove they are better than generic AI. |
| Start / end | Day 1 morning → Day 2 presentation |

Why this is a project:

- [x] Defined goal
- [x] Limited resources
- [x] Interdisciplinary
- [x] Responsibility for results
- [ ] Complex
- [x] Novel
- [x] Defined start/end

## 2. Objectives (Quality / Time / Cost)

| Constraint | Objective |
|---|---|
| Quality | Content the marketing team would publish after small edits; every product fact can be traced to the knowledge base, and nothing is invented. |
| Time | Hard deadline: Day 2 presentation. Internal milestone: working end-to-end draft by end of Day 1 (channel + product + topic in → post out, terminal). Day 2: feedback and improvement loop, Instagram, Gradio app, presentation. |
| Cost | gpt-4o-mini only, total API spend under €2, no paid tools; test calls limited to a fixed set of sample requests. |

## 3. Stakeholder analysis

Quadrants: I = high interest / high influence (manage closely) · II = low interest / high influence (keep satisfied) · III = high interest / low influence (keep informed) · IV = low interest / low influence (monitor).

| Role | Interest (H/L) | Influence (H/L) | Quadrant (I–IV) | Engagement in this project |
|---|---|---|---|---|
| Canyon marketing lead (non-builder, client) | H | H | I | Sets the quality bar; judges the generated content in the demo |
| Instructor / evaluator (non-builder) | H | H | I | Reviewed the scope on Day 1; grades repo, board and demo on Day 2 |
| Canyon content / social media team (non-builder, users) | H | L | III | Use the app daily; give feedback through the Day 2 feedback loop |
| Riders / Canyon customers (non-builder) | H | L | III | Read the posts and emails; affected by wrong product facts |
| Project team (3 students) | H | L | III | Build, review each other's cards, present |

## 4. Requirements → implementation

**Use case:** A Canyon marketer picks a channel (LinkedIn or email), a product family (gravel, road or mountain) and a topic, and gets ready-to-review content in Canyon's voice built from Canyon's real product facts.

**Must have:**

| ID | Must requirement | Maps to (file / module) | How we verify |
|---|---|---|---|
| M1 | Ingest primary KB markdown | `src/document_processor.py` + `knowledge_base/primary/` | Loader finds all primary files; every piece has a heading |
| M2 | Ingest secondary KB markdown | `src/document_processor.py` + `knowledge_base/secondary/` | Loader finds both secondary files |
| M3 | Call LLM with KB context | `src/llm_integration.py` | One real answer from the LLM; clear error message when the key is wrong |
| M4 | Reusable prompt templates (≥2) | `src/prompt_templates.py` + `templates/` (`system.txt`, `linkedin.txt`, `email.txt`) | Both templates fill; no `{...}` left in the prompt |
| M5 | End-to-end pipeline command | `src/content_pipeline.py` + `src/main.py` | `python src/main.py linkedin gravel "topic"` saves the approved post in `outputs/` |
| M6 | Uniqueness evidence vs ChatGPT | `uniqueness/comparison.md` | Same 3 requests (one per product family), generic vs our system, side by side |
| M7 | RAG decision documented | `rag_decision.md` | Choice + ≥3 criteria |
| M8 | Project structured + agents guided | `project_structure.md`, `agents.md` | All 7 sections complete; `agents.md` referenced in every coding-agent prompt |

**Should have (Day 2):** Instagram template · feedback and improvement loop (feedback → rewrite, feedback logged) · Gradio app.

**Won't have this sprint:**

| Won't | Why deferred |
|---|---|
| RAG / vector database | A few small markdown files fit in the prompt (see `rag_decision.md`) |
| Auto-publishing to LinkedIn or an email tool | A marketer always reviews and publishes (human in the loop) |
| Products beyond gravel, road and mountain bikes (e.g. e-bikes, accessories) | Keeps the knowledge base small and checkable in 2 days |
| Image or video generation | Output is written content only |

## 5. WBS (2 levels)

1. Structure & board
   - 1.1 Write `project_structure.md`
   - 1.2 Create Trello lists + WIP + DoD
   - 1.3 Write `agents.md`
   - 1.4 Create cards from this WBS
2. Knowledge bases
   - 2.1 Primary markdown set (brand voice, product specs for gravel / road / mountain, past marketing posts)
   - 2.2 Secondary markdown set (market trends, competitor marketing)
3. Ingest & context
   - 3.1 Markdown loader
   - 3.2 Context → prompts (pick brand voice + the chosen product + secondary)
4. Generate & differentiate
   - 4.1 LLM client + `.env`
   - 4.2 Prompt templates (LinkedIn + email)
   - 4.3 End-to-end pipeline command
   - 4.4 Uniqueness comparison artifact
5. Close
   - 5.1 Finalize `rag_decision.md` (+ structure §7)
   - 5.2 Day 2 extras: feedback loop + Instagram template + Gradio app
   - 5.3 README + demo prep
   - 5.4 Day 1 / Day 2 board screenshots

## 6. Risks

| Risk | Probability (L/M/H) | Impact (L/M/H) | Strategy | Concrete action |
|---|---|---|---|---|
| The AI invents product facts (specs, prices, features) *(technical)* | M | H | Reduction | System rule "use only knowledge base facts; never invent specs or prices"; test 3 requests before Day 2 noon |
| Product data for the 3 families is hard to collect or too thin *(process)* | M | M | Mitigation | Copy product pages into markdown by hand on Day 1; limit to one flagship model per family |
| Scope change on Day 1 afternoon delays the MVP *(process)* | H | H | Mitigation | Reuse the finished LLM client (4.1) and loader (3.1) unchanged; WIP limit 2; Day 2 extras cut first |

## 7. Bridge to RAG decision

The marketing lead's quality need is that every post uses Canyon's real product facts and voice, so the model must always see the brand guidelines and the full facts of the chosen product. Musts M1 to M3 load a small, stable knowledge base: about 6 markdown files covering three product families, which change only when Canyon updates a model. The request space is narrow (2 channels × 3 products × a topic), so simple rules pick the right pieces: brand voice and past posts always, plus the chosen product, plus all secondary context. Decision: inject the knowledge base into the prompt, no RAG (details in `rag_decision.md`). We would revisit this when the knowledge base grows to the full catalogue, multiple languages or long technical documents, or when the prompt gets too long or too expensive per request.
