---
title: "Mission 05 — RAG Engineering Knowledge Base"
project: "Aptech Enterprise AI Lab"
mission: "05"
version: "1.0"
updated: "2026-10-30"
status: "Living reference — code committed; learner runtime verification pending"
source_branch: "mission05-rag-grounded-answers"
tags: [rag, retrieval, grounding, fastapi, document-versioning, bug-004, evaluation]
---

# Mission 05 — RAG Engineering Knowledge Base

> **Purpose:** A durable, searchable technical reference for the concepts, implementation decisions, debugging patterns, and evidence gates in Mission 05. This is a companion to the Mission 05 self-learning Word guide, not a claim of production readiness.

## Navigation / retrieval index

| ID | Topic | Search terms |
|---|---|---|
| [M05-01](#m05-01-mission-story-and-scope) | Business problem and scope | support desk, policy, scenario |
| [M05-02](#m05-02-what-is-rag) | RAG fundamentals | retrieval augmented generation |
| [M05-03](#m05-03-architecture-and-data-flow) | Architecture | FastAPI, Agent, flow |
| [M05-04](#m05-04-document-ingestion-and-chunks) | Documents and chunks | ingestion, JSON, sections |
| [M05-05](#m05-05-lexical-retrieval-and-ranking) | Retrieval and ranking | token, overlap, top_k |
| [M05-06](#m05-06-metadata-freshness-and-eligibility) | Metadata and freshness | active, retired, effective |
| [M05-07](#m05-07-grounding-prompts-and-citations) | Grounding and citations | context, provenance, hallucination |
| [M05-08](#m05-08-fastapi-contracts) | API endpoints | rag/search, rag/ask, 422 |
| [M05-09](#m05-09-session-and-security-boundaries) | Session and security | Alice, Bob, auth, isolation |
| [M05-10](#m05-10-bug-004-investigation) | BUG-004 | outdated policy, root cause |
| [M05-11](#m05-11-tests-and-evidence) | Tests | FakeAgent, regression, Foundry |
| [M05-12](#m05-12-failure-modes-and-diagnostics) | Troubleshooting | no hits, 502, stale, prompt |
| [M05-13](#m05-13-production-rag-extensions-not-yet-implemented) | Future production extensions | embeddings, vectors, ACL |
| [M05-14](#m05-14-evaluation-and-metrics) | Evaluation | precision, recall, faithfulness |
| [M05-15](#m05-15-interview-defense-qa) | Interview Q&A | architecture, scenarios |
| [M05-16](#m05-16-hands-on-exercises-and-checklist) | Practice and release gates | commands, exercises |
| [M05-17](#m05-17-glossary) | Glossary | definitions |
| [M05-18](#m05-18-source-map-and-maintenance) | Sources and maintenance | code map, change log |

## M05-01 Mission story and scope

An internal support team repeatedly answers questions from employee policies. The repository already contains a Foundry Agent (Mission 01), a traced tool example (Mission 02), a per-user session router (Mission 03), and a FastAPI wrapper (Mission 04). Mission 05 adds a document retrieval boundary.

**Central incident:** a retired 2025 remote-work policy says **two days/week**; the active 2026 policy says **three days/week**. A fluent model answer is insufficient if the wrong version was supplied.

**Engineering objective:** prove which passages were eligible, selected, passed to the Agent, and returned as retrieval provenance. The code does not verify that each generated claim is supported.

**Learning method:** INHERIT → INVESTIGATE → MODIFY → BREAK → DIAGNOSE → FIX → DEFEND.

**Implemented:** synthetic JSON corpus, section chunks, deterministic lexical ranking, active-only filter, prompt context construction, three new RAG endpoints, offline tests, inherited Agent and in-process sessions.

**Not implemented:** embeddings, vector database, PDF/DOCX parsing, upload/ingestion endpoint, authentication, document ACLs, durable session storage, answer-level citation verification, production deployment. The workflow poster depicts some of these as *future architecture*, not current features.

## M05-02 What is RAG?

**Retrieval-Augmented Generation (RAG)** is an application pattern where relevant external information is retrieved and supplied to a generative model for a particular request.

Conceptual stages:
1. **Prepare** source documents for retrieval.
2. **Retrieve** passages relevant to a question.
3. **Augment** the model's request with those passages.
4. **Generate** an answer, ideally constrained to the evidence.
5. **Evaluate** whether the answer actually follows the evidence.

**RAG is not model training or fine-tuning.** It does not alter the model's weights. The retrieved context is supplied at inference time.

**RAG does not guarantee truth.** A wrong or outdated source, poor ranking, truncated context, ambiguous question, or model misinterpretation can still yield an incorrect answer.

**Example:** “How many days can employees work remotely?” The application retrieves the active policy's §3.2, then asks the Agent to answer using it. This is different from asking the model to recall an unspecified policy from its training data.

## M05-03 Architecture and data flow

```mermaid
flowchart TD
  U[Client question] --> API[FastAPI /rag/ask]
  API --> V[Pydantic validation]
  V --> R[retrieve question]
  KB[(Synthetic JSON policies)] --> C[load_chunks: one per section]
  C --> R
  R --> F{Active and relevant hits?}
  F -- No --> N[Cannot determine; no model call]
  F -- Yes --> P[build_grounded_prompt]
  P --> S[SessionRouter by caller user_id]
  S --> A[Inherited Foundry Agent]
  A --> O[Answer + retrieved source metadata]
  O --> U
```

**Important code distinction:** `/rag/search` stops after retrieval and does not invoke the model; `/rag/ask` calls the Agent if at least one hit exists.

**Source map:**
- `lab/mission-05/knowledge/policies.json` — synthetic policy data.
- `lab/mission-05/retrieval.py` — tokenization, chunk loading, retrieval, prompt.
- `lab/mission-05/service.py` — RAG API on top of the Mission 04 application factory.
- `lab/mission-04/service.py` — inherited `/health`, `/chat`, `/chat/stream` and Agent construction.
- `lab/mission-03/session_router.py` — per-user in-process session object mapping.
- `tests/test_mission05_rag.py` — offline regression.

## M05-04 Document ingestion and chunks

In production, ingestion may include parsing, cleaning, OCR, deduplication, version metadata, access permissions and indexing. **This lab does not implement that pipeline.** It reads a small, prestructured JSON file.

The JSON contains `id`, `title`, `status`, `effective`, and `sections` (each with `id` and `text`).

`load_chunks()` emits one record **per section**, with fields:

| Field | Meaning | Example |
|---|---|---|
| `source_id` | Stable document ID | `REMOTE-2026` |
| `title` | Human-readable document title | Remote Work Policy — current |
| `status` | Eligibility metadata | `active` |
| `effective` | Declared effective date | `2026-07-01` |
| `section` | Local section ID | `3.2` |
| `text` | Passage used for search and context | Three days/week |

**Chunking** splits a source into retrievable units. In this lab, section boundaries are already supplied. General RAG systems may chunk by paragraph, heading, sentence or token length, sometimes with overlap.

**Trade-off:** very small chunks can lose context; very large chunks can dilute ranking and consume context space. This pilot does not optimize chunk size.

## M05-05 Lexical retrieval and ranking

The implemented retriever is **lexical**, not semantic. It:
1. Lowercases input and extracts alphanumeric tokens with `[a-z0-9]+`.
2. Removes a small built-in stop-word set.
3. Creates token **sets** (repeated words do not increase score).
4. Scores each eligible chunk using the count of shared tokens between the query and the chunk's title + text.
5. Excludes zero-overlap chunks.
6. Sorts descending by score; ties sort ascending by `source_id`.
7. Returns at most `top_k` results, with `top_k` constrained to 1–10.

```python
score = len(tokens(question) & tokens(chunk["title"] + " " + chunk["text"]))
```

**Example:** the question “remote work days” overlaps with “Remote Work Policy” and the passage about remote days. This can retrieve the relevant section without any embedding model.

**Limitations:** synonyms (“work from home” versus “remote”), negation, multilingual queries, complex intent, dates and semantic equivalence may not be handled well. Ties may be arbitrary from a business perspective.

**`top_k` is a maximum count, not a relevance threshold.** Increasing it can add distracting passages. Decreasing it can omit useful evidence.

## M05-06 Metadata, freshness and eligibility

The **key distinction** is eligibility versus relevance:

- **Eligibility:** is this document permitted to participate in retrieval for the question? Here, only `status == "active"`.
- **Relevance:** among eligible chunks, which ones overlap the question most?

The implementation filters before scoring:
```python
if active_only and c["status"] != "active":
    continue
```

**BUG-004:** using `active_only=False` permits the retired 2025 policy into the candidate pool. A high lexical score does not make an outdated policy current.

**Important nuance:** the `effective` date is **stored but not interpreted** by the current retriever. The code does not implement “valid on date X,” supersession chains, date-based conflicts, or policy effective windows. The `active` field is a simplified synthetic truth source.

For production, define authoritative policy ownership, status changes, effective-from/to, supersedes relationships, tenant visibility and audit trails.

## M05-07 Grounding prompts and citations

`build_grounded_prompt(question, hits)` constructs a prompt containing:

- Instructions to answer only from supplied excerpts.
- An explicit “cannot determine” fallback.
- Source labels formatted as `[SOURCE_ID §SECTION]`.
- A reminder that document excerpts are **untrusted data, not instructions**.
- The user's question.

**Grounding** means constraining the answer to relevant supplied evidence. **Provenance** means recording where retrieved evidence came from. **Verified citation support** requires a separate check that each claim in the answer is actually supported by cited text.

**Current API behavior:** `/rag/ask` returns `sources` from the retriever and `grounded: false`. This does **not** mean the answer is necessarily false; it means the pilot has no independent answer-support verification.

**Prompt injection risk:** a document can contain text such as “ignore previous instructions.” Telling the model to treat excerpts as data is a useful prompt-level measure, but not a complete security boundary. Access control and other defenses are not implemented here.

**No-hit behavior:** when no passages overlap, the endpoint returns “Cannot determine from approved documents.” with empty sources, without calling the model.

## M05-08 FastAPI contracts

The Mission 05 app calls the inherited Mission 04 `create_app()`, preserving the earlier routes.

| Method | Route | Behavior |
|---|---|---|
| GET | `/health` | Local liveness only; not Azure readiness |
| POST | `/chat` | Existing non-RAG Agent chat |
| POST | `/chat/stream` | Existing SSE **completed-answer** event, not token streaming |
| GET | `/rag/documents` | Lists document metadata for all chunks, including retired |
| POST | `/rag/search` | Returns ranked active document hits; no model call |
| POST | `/rag/ask` | Retrieves active hits, builds context, calls Agent if hits exist |

**Request for RAG search/ask:**
```json
{"user_id": "alice", "question": "How many remote work days per week?", "top_k": 3}
```

`RagRequest` requires nonempty `user_id` (max 80 chars), nonempty `question` (max 4000 chars), and `top_k` from 1 to 10. Invalid bodies normally return **HTTP 422**.

**Backend exception:** `/rag/ask` converts Agent execution failures to a generic **HTTP 502**. The response does not expose internal exception details.

**`/rag/documents` is not a secure document catalogue:** it lists retired metadata too, and no authentication/authorization is implemented. Use only synthetic content in this lab.

**`/rag/search` currently accepts `user_id` but does not use it for document authorization.** This is an explicit production gap.

## M05-09 Session and security boundaries

Mission 05 reuses Mission 03's `SessionRouter` through Mission 04's application state. The application maps the caller's `user_id` to an in-memory session object.

**Positive test:** Alice can reuse her session.

**Negative test:** Bob receives a different session object.

**Critical:** `user_id` is a caller-supplied string, **not authenticated identity**. An attacker could claim another user's ID. The lab does not establish privacy or tenant isolation in a deployed environment.

The session map is per-process and is not durable. Multiple workers, concurrent requests, restart recovery, retention, authorization and secure shared storage require additional design.

RAG introduces a **second access-control boundary**: whether a user is permitted to retrieve a particular document. The current corpus is synthetic and has no ACL filtering.

## M05-10 BUG-004 investigation

**Symptom:** the Agent may answer “two days/week” even though the current policy says three.

**Competing hypotheses:**
1. The wrong (retired) source was eligible and retrieved.
2. The current source was retrieved but the Agent misread it.
3. Both sources were supplied and the prompt failed to resolve the conflict.
4. The user asked an ambiguous or historical question.

**Controlled reproduction:**
```python
chunks = load_chunks()
broken = retrieve("How many remote days per week?", chunks, active_only=False)
# Inspect whether REMOTE-2025 is included.
```

**Trace the earliest wrong boundary:** source status → candidate eligibility → ranking → context → Agent answer. In the lab, BUG-004 is reproduced by disabling the active-only filter, not by changing model instructions.

**Repair:** restore `active_only=True` and verify no retired source enters active retrieval results.

**Regression assertions:**
- Active query returns `REMOTE-2026`.
- Every returned hit has `status == "active"`.
- Deliberately broken retrieval can admit `REMOTE-2025`.
- `/rag/ask` supplies active source context.
- Empty input produces 422.
- Alice and Bob receive distinct session objects.

**Caveat:** the defect reproduction demonstrates stale **candidate inclusion**, not necessarily that the stale policy ranks first or that a live model actually gives the wrong answer.

## M05-11 Tests and evidence

**Offline test:** `python tests/test_mission05_rag.py`. Uses a FakeAgent, does not require Azure, and checks retrieval behavior, API contract and session object separation.

**Inherited regression:** `python tests/test_mission04_api.py` checks the earlier API's validation and session behavior.

**Environment verification:** `python scripts/verify_environment.py` checks configuration prerequisites; it does not prove a RAG response was generated.

**Live integration:** launch the Mission 05 API and call `/rag/ask` with a valid Foundry setup. Inspect response, sources, and backend errors. This remains a learner verification gate; a Git commit is not proof that the run succeeded.

**Evidence ledger template:**

| Test | Expected | Observed | Evidence link | Status |
|---|---|---|---|---|
| Offline retrieval | Only active sources | TBD | TBD | Pending |
| BUG-004 reproduction | Retired source admitted in broken mode | TBD | TBD | Pending |
| Request validation | 422 on empty question | TBD | TBD | Pending |
| No-match fallback | No Agent call; no sources | TBD | TBD | Pending |
| Alice/Bob routing | Distinct sessions | TBD | TBD | Pending |
| Live Foundry RAG | Answer and source provenance | TBD | TBD | Pending |

## M05-12 Failure modes and diagnostics

| Symptom | Inspect first | Interpretation / next step |
|---|---|---|
| No retrieval hits | Tokens, stop words, title/text | Lexical mismatch; do not blame the model |
| Retired policy in results | `active_only`, `status` | Eligibility defect; see BUG-004 |
| Both policy versions present | Metadata filter, corpus | Resolve source eligibility before prompt tuning |
| Wrong answer with correct hits | Prompt, actual context, model output | Generation/grounding issue |
| Source listed but answer unsupported | Claim-to-source evidence | Provenance is not verification |
| HTTP 422 | Request fields and bounds | Client validation issue |
| HTTP 502 | Agent/backend logs, credentials, endpoint | Backend execution failure |
| `/health` succeeds but `/rag/ask` fails | Foundry path | Liveness is not readiness |
| Bob inherits Alice context | Session routing, identity handling | Potential boundary failure; synthetic lab only |
| `/rag/search` exposes data to wrong user | Missing document ACL | Current design has no authorization |
| `/chat/stream` not token-by-token | Inherited Mission 04 implementation | Completed-answer SSE only |

## M05-13 Production RAG extensions not yet implemented

The following are **architecture concepts, not delivered features**:

1. **Document ingestion:** PDFs/DOCX/HTML, parsing, OCR if needed, cleaning, deduplication and versioning.
2. **Embeddings:** map text to numeric vectors to support semantic similarity.
3. **Vector search:** approximate nearest-neighbor indexes and similarity metrics.
4. **Hybrid retrieval:** combine lexical and vector results.
5. **Reranking:** use a separate ranking model to improve top passage ordering.
6. **Document-level ACLs:** filter by authenticated principal, tenant, classification and entitlements *before* retrieval.
7. **Freshness:** effective-date windows, supersession graphs, invalidation, deletion and reindexing.
8. **Answer verification:** claim-level support checks and citation validation.
9. **Operations:** monitoring, request correlation, evaluation suites, cost/latency budgets, retries and rate limits.
10. **Security:** secrets management, prompt-injection defenses, PII handling and audit trails.

**Concept distinction:** embedding generation converts text into vectors; a vector database stores/indexes them; a retriever selects candidates; a reranker reorders candidates; the LLM synthesizes an answer. These are separate responsibilities.

## M05-14 Evaluation and metrics

Evaluation should test retrieval and generation **separately**.

**Retrieval metrics (general concepts, not implemented):**
- **Recall@k:** fraction of relevant evidence captured in the top k.
- **Precision@k:** fraction of retrieved top-k passages that are relevant.
- **MRR:** reciprocal rank of the first relevant result, averaged across queries.
- **Freshness/eligibility rate:** percentage of returned documents meeting current/authorized rules.

**Generation metrics (general concepts, not implemented):**
- **Faithfulness / groundedness:** are answer claims supported by provided evidence?
- **Answer correctness:** does the response match a trusted expected answer?
- **Citation accuracy:** does each citation point to a supporting passage?
- **Abstention quality:** does the system decline when evidence is insufficient?

**System metrics:** latency p50/p95, retrieval time, token cost, error rate, zero-hit rate, stale-source rate and user feedback.

**Tiny evaluation set to create:**
| Query | Expected eligible source | Expected answer fact |
|---|---|---|
| How many remote days per week? | REMOTE-2026 §3.2 | Three with manager approval |
| When must travel claims be submitted? | EXPENSE-2026 §2.1 | Within 30 calendar days |
| What is the cafeteria menu? | None | Cannot determine |

The actual pilot test does not automatically score all these answer-level expectations.

## M05-15 Interview defense Q&A

**Q1. What problem does RAG solve?** It supplies selected external evidence at request time, allowing an Agent to answer from application-controlled information rather than relying only on model knowledge.

**Q2. Does RAG prevent hallucinations?** No. It can improve grounding but can also retrieve wrong data or produce unsupported conclusions.

**Q3. Why filter inactive documents before ranking?** A highly relevant retired document must not outrank an eligible current document simply because its words match.

**Q4. Why use lexical retrieval first?** It is deterministic and inspectable for learning. It is weaker on synonyms and semantics than vector/hybrid approaches.

**Q5. What does `top_k` control?** Maximum number of ranked passages returned, not guaranteed relevance or truth.

**Q6. What is the difference between a source ID and a verified citation?** A source ID shows retrieval provenance; a verified citation establishes that a particular claim is supported by a particular passage.

**Q7. What is BUG-004?** Retired content enters retrieval when the active-status eligibility filter is disabled.

**Q8. Why might `/rag/ask` return 502?** The Agent/backend failed after request validation; investigate credentials, model endpoint and runtime errors internally.

**Q9. How is this different from fine-tuning?** RAG changes the context supplied at inference time; fine-tuning changes model weights.

**Q10. Can this support multiple authenticated tenants?** Not as implemented. The pilot lacks authentication, document ACLs and durable multiworker session design.

**Q11. Why return `grounded:false`?** The system has not independently verified that the generated answer is supported by the retrieved passages.

**Q12. What would you build next inside RAG?** A controlled evaluation set, document authorization, version-aware filtering, then embeddings/hybrid retrieval as evidence justifies complexity.

## M05-16 Hands-on exercises and checklist

Run from the existing local repository (Windows PowerShell):

```powershell
cd C:\ai-labs-isoft\aptech-enterprise-ai-lab
git fetch origin
git switch mission05-rag-grounded-answers
# If branch does not exist locally:
# git switch --track origin/mission05-rag-grounded-answers

.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python tests/test_mission04_api.py
python tests/test_mission05_rag.py
python scripts/verify_environment.py
python -m uvicorn service:app --app-dir lab/mission-05 --reload
```

Visit `http://127.0.0.1:8000/docs` and call:
- `GET /rag/documents` — inspect metadata and retired documents.
- `POST /rag/search` — see which passages are selected before generation.
- `POST /rag/ask` — invoke the Agent with the selected passages.

**Exercises:**
1. Sketch the pipeline and annotate each component with its source file.
2. Predict the active remote-work result; run retrieval and compare.
3. Reproduce BUG-004 with `active_only=False`; capture returned IDs.
4. Restore the filter and rerun tests.
5. Submit an empty question and explain HTTP 422.
6. Submit an unrelated question and inspect no-hit abstention.
7. Compare two user IDs and identify the session routing boundary.
8. Explain why no-hit, no-source, and `grounded:false` are distinct states.
9. Propose one test for effective-date handling (not implemented).
10. Present a 90-second incident defense with code and evidence.

**Release gate:** offline tests + live Foundry integration + source inspection + BUG-004 reproduction/repair + review. Do not merge based solely on authored code.

## M05-17 Glossary

| Term | Definition |
|---|---|
| RAG | Retrieval-Augmented Generation: retrieve external context before generation |
| Corpus | Collection of documents available for retrieval |
| Ingestion | Process of loading/preparing documents for indexing |
| Chunk | Retrievable text unit, here a policy section |
| Metadata | Attributes such as source ID, status, date and section |
| Lexical retrieval | Matching based on word/token overlap |
| Semantic retrieval | Retrieving by meaning, often via embeddings |
| Embedding | Numeric representation of text or another object |
| Vector index | Data structure supporting similarity search over embeddings |
| Hybrid search | Combining lexical and semantic retrieval |
| Reranker | Component that reorders retrieved candidates |
| `top_k` | Maximum number of returned retrieval hits |
| Grounding | Connecting answer claims to supplied evidence |
| Provenance | Origin information for a retrieved passage |
| Citation verification | Checking that a cited passage supports an answer claim |
| Abstention | Declining to answer when evidence is insufficient |
| Prompt injection | Malicious instructions embedded in lower-trust content |
| ACL | Access-control list governing which documents a principal may access |
| Regression test | Test that catches recurrence of a known defect |
| FakeAgent | Local test double replacing the live Foundry Agent |
| HTTP 422 | Request-body validation failure |
| HTTP 502 | Generic backend execution failure in this pilot |
| SessionRouter | In-process mapping from caller-provided user ID to session object |

## M05-18 Source map and maintenance

### Primary repository sources

- `lab/mission-05/README.md` — scope, commands and BUG-004.
- `lab/mission-05/retrieval.py` — exact lexical algorithm.
- `lab/mission-05/knowledge/policies.json` — synthetic current/retired facts.
- `lab/mission-05/service.py` — FastAPI contract and Agent call.
- `tests/test_mission05_rag.py` — what offline tests actually assert.
- `lab/mission-04/service.py` — inherited API and Foundry Agent factory.
- `lab/mission-03/session_router.py` — inherited session routing.
- `docs/milestones/MILESTONE-05.md` — release/evidence notes.
- `Aptech_AI_Lab_Milestone_05_Self_Learning_Guide.docx` — companion narrative document.

### Update rules

1. Preserve stable `M05-XX` identifiers so references remain searchable.
2. Update **Implemented / Not implemented** when code changes.
3. Add source paths and tests whenever a capability is added.
4. Record learner runtime results only after they are actually observed.
5. Keep production proposals separate from current code claims.
6. Add new incidents as `BUG-005` etc. only when the mission numbering plan is approved.
7. Use concise change log entries and do not overwrite prior evidence.

### Change log

| Date | Version | Change |
|---|---|---|
| 2026-10-30 | 1.0 | Initial Mission 05 concept reference, code map, BUG-004, evaluation and evidence gates |
