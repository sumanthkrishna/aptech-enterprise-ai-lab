# Aptech Enterprise AI Lab — Living Knowledge Library

This is the reading path for the Aptech Enterprise AI Lab. Start with Mission 01, get its sample running, and move forward only when you can explain what the code does and what your tests actually prove. Each mission links to the implementation branch, the relevant source files, a defect investigation, and a set of checks you can run yourself.

## New learner? Start with the frozen baseline

Read [START-HERE](../../START-HERE.md), then check out [`release/starter-v1`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/release/starter-v1). The starter is a clean Mission 01 entry point; it won't move as later missions are merged. Work on your own `learner/*` branch. The mission branches stay available as reference implementations, and `main` will hold the combined code after the PRs merge.

## Learning path

| Order | Mission | Living reference | Main learning objective | Controlled defect |
|---|---|---|---|---|
| 01 | Know Your System | [Agent foundations](MISSION-01-AGENT-FOUNDATIONS-KNOWLEDGE-BASE.md) | Foundry Agent, client, credentials, configuration | Baseline and configuration investigation |
| 02 | Give the Agent a Tool | [Agent tools](MISSION-02-AGENT-TOOLS-KNOWLEDGE-BASE.md) | Tool registration and output inspection | BUG-001: unrealistic synthetic result |
| 03 | What Does the Agent Remember? | [Session isolation](MISSION-03-SESSION-ISOLATION-KNOWLEDGE-BASE.md) | Same-user continuity and cross-user isolation | BUG-002: wrong session routing |
| 04 | Turn Your Agent into an API | [FastAPI service](MISSION-04-FASTAPI-AGENT-SERVICE-KNOWLEDGE-BASE.md) | HTTP validation, sessions, error boundaries, SSE | BUG-003: hypothetical global session |
| 05 | Make Your Agent Answer from Documents | [RAG knowledge base](MISSION-05-RAG-KNOWLEDGE-BASE.md) | Retrieval, freshness, grounding, source provenance | BUG-004: retired policy inclusion |

## Branch map and source of truth

| Mission | Implementation branch | Verified entry point | Documentation |
|---|---|---|---|
| 01 | [release/starter-v1](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/release/starter-v1) | [01_hello_agent.py](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/main/lab/mission-01/01_hello_agent.py) | [M01 reference](MISSION-01-AGENT-FOUNDATIONS-KNOWLEDGE-BASE.md) |
| 02 | [mission02-investigate-tool-path](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission02-investigate-tool-path) | [02_add_tools.py](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission02-investigate-tool-path/lab/mission-02/02_add_tools.py) | [M02 reference](MISSION-02-AGENT-TOOLS-KNOWLEDGE-BASE.md) |
| 03 | [mission03-session-isolation](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission03-session-isolation) | [03_multi_turn.py](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission03-session-isolation/lab/mission-03/03_multi_turn.py) | [M03 reference](MISSION-03-SESSION-ISOLATION-KNOWLEDGE-BASE.md) |
| 04 | [mission04-fastapi-agent-service](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission04-fastapi-agent-service) | [service.py](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission04-fastapi-agent-service/lab/mission-04/service.py) | [M04 reference](MISSION-04-FASTAPI-AGENT-SERVICE-KNOWLEDGE-BASE.md) |
| 05 | [mission05-rag-grounded-answers](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission05-rag-grounded-answers) | [service.py](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission05-rag-grounded-answers/lab/mission-05/service.py) | [M05 reference](MISSION-05-RAG-KNOWLEDGE-BASE.md) |

**Provenance:** Mission 01's baseline originally lived on `main` and is now preserved on `release/starter-v1`; the other four mission branches were confirmed. The five *living reference documents* are centralized on the Mission 05 branch, with direct links to the matching source branch. Earlier branches are not rewritten. This keeps mission history intact and avoids adding competing copies of the same documentation.

## How to work through a mission

Read the story first, then open the code. Try to predict what the program will do before you run it. When something fails, write down your hypothesis and test the earliest boundary that could explain it. Keep the terminal output; you'll need it when you explain your fix.

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

## Integration and release policy

- Keep `release/starter-v1` as the frozen newcomer baseline. Don't add future missions to it.
- Keep the original `missionXX-*` branches unchanged after they are merged. Learners should create their own `learner/*` branches for exercises.
- Merge the prepared integration PRs into `main` in this order: [#2](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/2), [#7](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/7), [#8](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/8), then [#9](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/9). Integration branches inherit their predecessor's code and reconcile shared files without changing the original mission branches.
- The prepared integration PRs already target `main`. After each predecessor merges, recheck the next PR's diff and GitHub mergeability before clicking Merge. PRs #8 and #9 remain drafts until verification gates are addressed.
- Prefer merge commits where preserving controlled broken/fixed history matters. Avoid squash-merging those teaching histories.
- Create an immutable release tag after a verified foundation or platform milestone. Use release branches only when a checkpoint needs continuing maintenance.
- Keep offline and live verification states explicit. Do not merge a draft PR merely because GitHub reports it as mergeable.

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

The references for Missions 01–04 were created from available repository source files; Mission 05 was created earlier. Mission 01's runnable sample was confirmed as `lab/mission-01/01_hello_agent.py` on `main`. The references are a starting knowledge library, not a claim that every mission has been independently runtime-verified.

**Evidence still needed:** actual learner test results and Foundry transcripts. Those should be added when observed, rather than written as if the runs already happened.

## Change log

| Date | Change |
|---|---|
| 2026-10-30 | Initial library index for living Mission 01–05 knowledge references |
| 2026-10-30 | Humanized introduction and learner instructions; branch links preserved |
| 2026-10-30 | Added frozen starter checkpoint, learner branch workflow, and merge/release policy |

## Prepared merge queue (2026-10-30)

| Order | PR | Integration branch | Action |
|---|---|---|---|
| 1 | [#2](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/2) | `mission02-investigate-tool-path` | Merge first |
| 2 | [#7](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/7) | `integration/mission03-on-mission02` | Merge after #2 |
| 3 | [#8](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/8) | `integration/mission04-on-mission03` | Draft; verify then merge after #7 |
| 4 | [#9](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/pull/9) | `integration/mission05-on-mission04` | Draft; verify then merge after #8 |

Original PRs #3–#5 were closed as superseded, not merged. Their original mission branches remain intact. This queue is designed to avoid the competing shared-file edits found between Missions 02 and 03. GitHub mergeability must be checked again after each merge; current checks are not a guarantee about future repository changes.
