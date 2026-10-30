# Aptech Enterprise AI Lab

A 40-hour enterprise AI lab built around real engineering habits: read inherited code, reproduce a problem, trace its cause, make a small repair, and prove it works.

## Self-learning curriculum

Start with the [Living Knowledge Library](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission05-rag-grounded-answers/docs/knowledge/README.md). It connects Missions 01–05 to their respective source branches, source files, defects, tests, and next/previous references. The library currently lives on the Mission 05 branch pending a merge decision; the link is branch-specific by design.

## Pilot scope

Agentic AI Track v0.1 (Missions 04–05 also available on their feature branches):
- Mission 01 — Know Your System
- Mission 02 — Give the Agent a Tool
- Mission 03 — What Does the Agent Remember?
- BUG-001 — Incorrect tool result
- BUG-002 — Session mix-up

## Learning method

**ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**

Start from a working sample. Find out why it works, change one thing at a time, and keep evidence when something breaks. The goal is to explain your decisions to another engineer, not just get an answer from the Agent.

## Upstream

Initial lab samples are adapted from Microsoft Agent Framework. See `UPSTREAM.md` and `LICENSES/MICROSOFT_AGENT_FRAMEWORK_MIT.txt`.

## Layout

- `lab/` runnable learner-facing samples
- `training/missions/` mission briefs
- `defects/` seeded defect scenarios
- `tests/` validation/regression checks
- `scripts/` setup/reset/verification
- `docs/` setup, architecture, troubleshooting
- `instructor/` instructor-only guidance/solutions

**Status:** v0.1 pilot under construction.
