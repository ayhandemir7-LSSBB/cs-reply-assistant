# project_structure.md: AI Content Creator

## 1. Project identity

| Item | Answer |
|---|---|
| Project name | AI Content Creator (demo client: Canyon Bicycles) |
| Primary project type | Organizational; the knowledge base can be replaced for another company, with its facts and prompts reviewed before use. |
| Defined goal | Give Canyon's marketing team email, Instagram, LinkedIn, and newsletter drafts in English, German, French, and Spanish about gravel, road, and mountain bikes, using Canyon's voice and product knowledge; compare product grounding with generic AI. |
| Planned start / end | Day 1 morning → Day 2 presentation. Actual dates and completion time are not recorded here. |

Why this is a project:

- [x] Defined goal
- [x] Limited resources
- [x] Interdisciplinary
- [x] Responsibility for results
- [ ] Complex
- [x] Novel
- [x] Defined start/end

## 2. Objectives (Quality / Time / Cost)

| Constraint | Objective | Closeout evidence |
|---|---|---|
| Quality | Drafts should use Canyon's voice and traceable product facts; a person reviews every draft before saving. | The comparison report records examples of stronger product grounding as well as unsupported claims, lost qualifications, and style or length failures. The quality target is not fully demonstrated. |
| Time | Plan: end-to-end terminal draft by the end of Day 1; feedback loop, Instagram, Gradio app, and presentation on Day 2. | Actual dates, duration, and schedule variance are not recorded. |
| Cost | Plan: total API spend under €2, no paid tools, and a fixed set of test requests. `LLM_MODEL` is configurable in `.env` and defaults to `gpt-4o-mini`. | Actual API spend and final model setting are not recorded here. The planned budget is not a reported actual. |

## 3. Stakeholder analysis

Quadrants: I = high interest / high influence (manage closely) · II = low interest / high influence (keep satisfied) · III = high interest / low influence (keep informed) · IV = low interest / low influence (monitor).

| Role | Interest | Influence | Quadrant | Engagement |
|---|---|---|---|---|
| Canyon marketing lead (client) | H | H | I | Sets the quality bar and reviews the demo. |
| Instructor / evaluator | H | H | I | Reviews the project plan, repository, board, and demo. |
| Canyon content / social media team (intended users) | H | L | III | Intended users of the draft and feedback workflow; production use is not documented. |
| Riders / Canyon customers (audience) | H | L | III | Intended readers of generated content; factual errors could affect trust. |
| Project team (3 students) | H | L | III | Builds, reviews work, and presents the project. |

## 4. Requirements → implementation

**Use case:** A Canyon marketer chooses a channel (email, Instagram, LinkedIn, newsletter), product family (gravel, road, mountain), language (English, German, French, Spanish), and topic, then reviews a draft grounded in selected product facts.

**Must have:**

| ID | Requirement | Implementation | How to verify | Recorded status / evidence |
|---|---|---|---|---|
| M1 | Ingest primary knowledge-base Markdown | `src/document_processor.py`, `knowledge_base/primary/` | Loader finds primary files and gives each piece a heading. | README records local document-processor and knowledge-base checks as passed. |
| M2 | Ingest secondary knowledge-base Markdown | `src/document_processor.py`, `knowledge_base/secondary/` | Loader finds both secondary files. | README records local document-processor and knowledge-base checks as passed. |
| M3 | Call the LLM with knowledge-base context | `src/llm_integration.py` | Obtain a real answer and confirm a clear error for an invalid key. | The recorded local review skipped live LLM calls; the real-answer and invalid-key checks are not evidenced there. |
| M4 | Reusable channel templates and language selection | `src/prompt_templates.py`, `templates/` | Build every channel/language prompt with no unresolved fields. | README records the prompt-template check as passed. |
| M5 | End-to-end pipeline command | `src/content_pipeline.py`, `src/main.py` | Generate, review, approve, and confirm the language-coded file in `outputs/`. | CLI usage check is recorded as passed and output files exist; this document does not record a repeatable end-to-end approval/save check. |
| M6 | Compare product grounding with generic AI | `uniqueness/comparison.md` | Review five fixed requests across three product families and four channels. | Comparison artifacts are present and document both grounding examples and limitations. |
| M7 | Document the retrieval decision | `rag_decision.md` | Document the approach and at least three criteria. | Decision document is present; it labels its status “Proposed for team review and approval.” |
| M8 | Structure the project and guide coding agents | `project_structure.md`, `agents.md` | Complete the seven sections and reference `agents.md` in coding-agent prompts. | Both documents are present, but this plan retains unresolved timing and Render-status TODOs. |

**Should-have (implemented in the repository):** feedback logging and rewrite flow · Instagram and newsletter templates · four output languages · quality check · Gradio app.

**Won't have this sprint:**

| Won't | Why deferred |
|---|---|
| RAG / vector database | The current implementation uses explicit selection and direct prompt context; see `rag_decision.md`. |
| Auto-publishing to LinkedIn or an email tool | A person reviews and publishes content. |
| Products beyond gravel, road, and mountain bikes | Keeps the project scope focused and checkable. |
| Image or video generation | This project generates written content. |

## 5. Work breakdown and closeout

1. Structure & board
   - 1.1 Write `project_structure.md`
   - 1.2 Create Trello lists, WIP limit, and Definition of Done
   - 1.3 Write `agents.md`
   - 1.4 Create cards from this WBS
2. Knowledge bases
   - 2.1 Primary Markdown set (brand voice and product specs for gravel / road / mountain)
   - 2.1b Past marketing posts (one file per post)
   - 2.2 Secondary Markdown set (market trends and competitor marketing)
3. Ingest & context
   - 3.1 Markdown loader
   - 3.2 Context selection for prompts
4. Generate & differentiate
   - 4.1 LLM client and `.env`
   - 4.2 Prompt templates (channels and four languages)
   - 4.2b Template rework and shared banned-phrase rules
   - 4.3 End-to-end pipeline command
   - 4.4 Uniqueness comparison artifact
5. Close
   - 5.1 Finalize `rag_decision.md` and project-structure section 7
   - 5.2 Day 2 additions: feedback, templates, languages, quality check, and Gradio app
     - 5.2a Feedback loop and log
     - 5.2b Instagram and newsletter templates
     - 5.2c Four-language support and quality check
     - 5.2d Gradio app
   - 5.3 README and demo preparation
   - 5.4 Day 1 / Day 2 board screenshots
   - 5.5 Render deployment (status and URL not recorded)

The 5.2a–5.2d entries are subtasks under 5.2, so the WBS has more than two levels.

**Closeout evidence in the repository:** comparison reports, saved draft files, a feedback log, and Day 1 / Day 2 board screenshots are present. The actual schedule and API spend, formal approval of the RAG decision, Render deployment status/URL, and demo plan are not recorded.

## 6. Risks and follow-up

| Concern | Evidence at closeout | Follow-up |
|---|---|---|
| Generated content may contain unsupported or overbroad claims. | The comparison documents unsupported generic claims and qualification/style issues in generated drafts. The style check does not verify facts. | Keep human review; check product identity, specifications, units, and qualifications against the knowledge base before publication. |
| Knowledge-base coverage or freshness may be incomplete. | The repo contains brand, product, past-content, and secondary Markdown; a completeness or freshness review is not recorded here. | Have the content owner confirm source coverage and update dates before expanding use. |
| API behavior and deployment are not fully evidenced by the recorded checks. | README says live LLM calls were skipped; the Render status/URL is not recorded. | Record a real API check and deployment result before describing the service as live or production-ready. |
| The original schedule and scope risks have no retrospective outcome. | Actual dates, schedule variance, and scope impact are not recorded. | Add those outcomes if project records are available; do not treat planning probabilities as current estimates. |

## 7. Bridge to RAG decision

The current implementation reads Markdown, selects product-spec sections by the chosen family, includes brand guidelines, past examples, and secondary context, then inserts that material into the prompt. Selection is not based on topic, channel, or language. This describes the implementation; it does not mean the retrieval decision received formal approval. `rag_decision.md` records the rationale, seven criteria, limits, and conditions for revisiting the approach, and currently labels its status as proposed for team review.
