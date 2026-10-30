# Aptech Enterprise AI Lab — Living Knowledge Library

**Purpose:** self-guided, source-linked enterprise AI engineering curriculum. Start at Mission 01 and progress in order. Each mission has a living Markdown reference, runnable code, investigation exercise, and evidence gate.

## Learning path

| Order | Mission | Living reference | Main learning objective | Controlled defect |
|---|---|---|---|---|
| 01 | Know Your System | [Agent foundations](MISSION-01-AGENT-FOUNDATIONS-KNOWLEDGE-BASE.md) | Foundry Agent, client, credentials, configuration | Baseline and configuration investigation |
| 02 | Give the Agent a Tool | [Agent tools](MISSION-02-AGENT-TOOLS-KNOWLEDGE-BASE.md) | Tool registration and output inspection | BUG-001: unrealistic synthetic result |
| 03 | What Does the Agent Remember? | [Session isolation](MISSION-03-SESSION-ISOLATION-KNOWLEDGE-BASE.md) | Same-user continuity and cross-user isolation | BUG-002: wrong session routing |
| 04 | Turn Your Agent into an API | [FastAPI service](MISSION-04-FASTAPI-AGENT-SERVICE-KNOWLEDGE-BASE.md) | HTTP validation, sessions, error boundaries, SSE | BUG-003: hypothetical global session |
| 05 | Make Your Agent Answer from Documents | [RAG knowledge base](MISSION-05-RAG-KNOWLEDGE-BASE.md) | Retrieval, freshness, grounding, source provenance | BUG-004: retired policy inclusion |

## How to study each mission

1. **Read** the mission story and concept glossary.
2. **Inspect** the linked source files before changing code.
3. **Predict** behavior and write a hypothesis.
4. **Run** the baseline and capture evidence.
5. **Reproduce** the controlled defect or scenario.
6. **Repair** the earliest incorrect boundary.
7. **Test** both the positive and negative cases.
8. **Defend** the fix in an interview-style explanation.
9. **Record** what is proven, what remains pending, and what is not implemented.

> **Rule:** An AI-generated answer is not evidence. Source code, traces, reproducible tests and observed integration behavior are evidence.

## Repository orientation

- `lab/` — runnable samples and shared components
- `tests/` — offline regression checks
- `training/missions/` — learner mission briefs where available
- `docs/milestones/` — milestone acceptance/evidence notes where available
- `docs/knowledge/` — this living, searchable concept library
- `scripts/` — environment and verification helpers
- `defects/` — investigation material where available

## Verification boundaries

**Do not claim** that a document or committed test has run successfully. Offline checks and live Azure Foundry calls are separate gates. Caller-supplied user IDs are not authentication. In-memory sessions are not durable memory. Mission 05 lexical retrieval is not embeddings/vector search, and retrieved source metadata is not independently verified answer support.

## Contribution and maintenance policy

- Preserve stable identifiers such as `M03-07` for links and retrieval.
- Change the implementation description only after inspecting code.
- Keep **implemented**, **proposed**, **tested offline**, and **verified live** distinct.
- Update the relevant mission reference and its tests in the same PR as a code change.
- Add troubleshooting examples, failed hypotheses and evidence links.
- Use synthetic data for controlled incidents.
- Maintain a short change log at the end of each reference.
- Do not rewrite past incident evidence to make a new design appear correct.

## Current coverage and gaps

The references for Missions 01–04 were created from available repository source files; Mission 05 was created earlier. Mission 01's exact runnable sample path was **not confirmed** during this documentation pass, so its reference explicitly calls for locating it before running. The references are a starting knowledge library, not a claim that every mission has been independently runtime-verified.

**Next editorial improvements:** confirm Mission 01's runnable sample path, add real observed test evidence and screenshots/terminal transcripts, and expand individual sections as learners raise questions.

## Change log

| Date | Change |
|---|---|
| 2026-10-30 | Initial library index for living Mission 01–05 knowledge references |
