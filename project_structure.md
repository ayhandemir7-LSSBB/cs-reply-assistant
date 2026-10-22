# project_structure.md: CS Reply Assistant

## 1. Project identity

| Item | Answer |
|---|---|
| Project name | CS Reply Assistant (demo client: Canyon Bicycles) |
| Primary project type | Organizational (reusable for any organisation by replacing the knowledge base files) |
| Defined goal | Give Canyon customer service agents draft replies in Canyon's voice, based only on Canyon's real policies, and prove they are better than generic AI. |
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
| Quality | Draft replies a CS agent can send after small edits; every policy fact can be traced to the knowledge base, and nothing is invented. |
| Time | Hard deadline: Day 2 presentation. Internal milestone: working end-to-end draft by end of Day 1 (customer message in → reply out, terminal). Day 2: improvements, Gradio app, feedback logging, presentation. |
| Cost | gpt-4o-mini only, total API spend under €2, no paid tools; test calls limited to a fixed set of sample messages. |

## 3. Stakeholder analysis

Quadrants: I = high interest / high influence (manage closely) · II = low interest / high influence (keep satisfied) · III = high interest / low influence (keep informed) · IV = low interest / low influence (monitor).

| Role | Interest (H/L) | Influence (H/L) | Quadrant (I–IV) | Engagement in this project |
|---|---|---|---|---|
| Canyon CS team lead (non-builder, client) | H | H | I | Sets the quality bar; judges the draft replies in the demo |
| Instructor / evaluator (non-builder) | H | H | I | Reviews the plan on Day 1; grades repo, board and demo on Day 2 |
| Canyon CS agents (non-builder, users) | H | L | III | Use the drafts; give feedback through the Day 2 feedback log |
| Canyon customers (non-builder) | H | L | III | Receive the final replies; most affected by a wrong policy fact |
| Project team (3 students) | H | L | III | Build, review each other's cards, present |

## 4. Requirements → implementation

**Use case:** A Canyon CS agent pastes a customer message, picks the channel (email or chat), and gets a draft reply in Canyon's voice that uses only Canyon's real policies.

**Must have:**

| ID | Must requirement | Maps to (file / module) | How we verify |
|---|---|---|---|
| M1 | Ingest primary KB markdown | `src/document_processor.py` + `knowledge_base/primary/` | Loader finds all primary files; every piece has a heading |
| M2 | Ingest secondary KB markdown | `src/document_processor.py` + `knowledge_base/secondary/` | Loader finds both secondary files |
| M3 | Call LLM with KB context | `src/llm_integration.py` | One real reply from the LLM; clear error message when the key is wrong |
| M4 | Reusable prompt templates (≥2) | `src/prompt_templates.py` + `templates/` (`system.txt`, `email_reply.txt`, `chat_reply.txt`) | Both templates fill; no `{...}` left in the prompt |
| M5 | End-to-end pipeline command | `src/content_pipeline.py` + `src/main.py` | `python src/main.py "customer message" email` saves an approved reply in `outputs/` |
| M6 | Uniqueness evidence vs ChatGPT | `uniqueness/comparison.md` | Same 3 customer messages (return, delayed delivery, warranty), generic vs our system, side by side |
| M7 | RAG decision documented | `rag_decision.md` | Choice + ≥3 criteria |
| M8 | Project structured + agents guided | `project_structure.md`, `agents.md` | All 7 sections complete; `agents.md` referenced in every coding-agent prompt |

**Won't have this sprint:**

| Won't | Why deferred |
|---|---|
| RAG / vector database | A few small markdown files fit in the prompt (see `rag_decision.md`) |
| Sending replies to customers automatically | The agent always reviews and sends (human in the loop) |
| Integration with a real ticket system or CRM (e.g. Zendesk) | Too large for 2 days; not needed to prove the concept |
| Real customer data | GDPR; all test messages are invented |

## 5. WBS (2 levels)

1. Structure & board
   - 1.1 Write `project_structure.md`
   - 1.2 Create Trello lists + WIP + DoD
   - 1.3 Write `agents.md`
   - 1.4 Create cards from this WBS
2. Knowledge bases
   - 2.1 Primary markdown set (brand voice, products, CS policies, sample replies)
   - 2.2 Secondary markdown set (market trends, competitor service policies)
3. Ingest & context
   - 3.1 Markdown loader
   - 3.2 Context → prompts
4. Generate & differentiate
   - 4.1 LLM client + `.env`
   - 4.2 Prompt templates (email + chat)
   - 4.3 End-to-end pipeline command
   - 4.4 Uniqueness comparison artifact
5. Close
   - 5.1 Finalize `rag_decision.md` (+ structure §7)
   - 5.2 Gradio app + feedback log (Day 2)
   - 5.3 README + demo prep
   - 5.4 Day 1 / Day 2 board screenshots

## 6. Risks

| Risk | Probability (L/M/H) | Impact (L/M/H) | Strategy | Concrete action |
|---|---|---|---|---|
| The AI invents a policy (wrong return window, refund or warranty terms) *(technical)* | M | H | Reduction | System rule "use only knowledge base facts; if a fact is missing, tell the agent to check"; test with 3 policy questions before Day 2 noon |
| Canyon FAQ data is hard to collect or incomplete *(process)* | M | M | Mitigation | Copy the FAQ into markdown by hand on Day 1 morning; fill gaps from EU consumer rules, marked as general information |
| Too many open tasks, MVP not ready by end of Day 1 *(process)* | M | H | Mitigation | WIP limit 2; split large cards; Gradio and feedback logging stay on Day 2; cut Shoulds before Musts |

## 7. Bridge to RAG decision

The CS team lead's quality need is that every reply uses Canyon's real policies and never invents one, so the model must always see the complete policy and brand voice context. Musts M1 to M3 load a small, stable knowledge base: about 7 markdown files that change only when Canyon updates its FAQ. All of it fits in one prompt at low cost, so retrieval would add complexity (chunking, embeddings, a vector store) without improving the replies in 2 days. Decision: inject the knowledge base into the prompt, no RAG (details in `rag_decision.md`). We would revisit this when the knowledge base grows to the full help centre, multiple languages or product manuals, or when the prompt gets too long or too expensive per reply.
