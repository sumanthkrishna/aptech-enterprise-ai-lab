---
title: "Mission 02 – Give the Agent a Tool"
project: "Aptech Enterprise AI Lab"
mission: "02"
version: "1.1"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-02, self-learning]
---

# Mission 02 – Give the Agent a Tool

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Mission navigation and branch provenance

**Documentation home:** [Living Knowledge Library](./README.md) (maintained on `mission05-rag-grounded-answers`).  
**Mission implementation branch:** [`mission02-investigate-tool-path`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/mission02-investigate-tool-path).  
**Verified entry point:** [`lab/mission-02/02_add_tools.py`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission02-investigate-tool-path/lab/mission-02/02_add_tools.py).  
**Learning sequence:** [← Mission 01](./MISSION-01-AGENT-FOUNDATIONS-KNOWLEDGE-BASE.md) · [Mission 03 →](./MISSION-03-SESSION-ISOLATION-KNOWLEDGE-BASE.md).

**Version-control note:** Mission 01's baseline is frozen on `release/starter-v1` (created from `main` before the mission merges). Mission 02–05 have individual branches. These knowledge documents are consolidated on the Mission 05 branch and link to each mission's implementation branch; they have **not** been copied into every earlier branch. No merges are performed by documentation updates.


## Retrieval index

| ID | Topic |
|---|---|
| [M02-01](#m02-01-story-and-outcome) | Story and outcome |
| [M02-02](#m02-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M02-03](#m02-03-architecture) | Architecture |
| [M02-04](#m02-04-core-concepts) | Core concepts |
| [M02-05](#m02-05-code-to-concept-map) | Code-to-concept map |
| [M02-06](#m02-06-execution-lifecycle) | Execution lifecycle |
| [M02-07](#m02-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M02-08](#m02-08-hands-on-verification) | Hands-on verification |
| [M02-09](#m02-09-troubleshooting) | Troubleshooting |
| [M02-10](#m02-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M02-11](#m02-11-interview-defense) | Interview defense |
| [M02-12](#m02-12-glossary) | Glossary |
| [M02-13](#m02-13-review-checklist) | Review checklist |
| [M02-14](#m02-14-maintenance-and-references) | Maintenance and references |

## M02-01 Story and outcome

The Agent can now call Python code to get information it doesn't have in the conversation. The sample uses weather because the tool is easy to inspect. Its data is deliberately synthetic: random conditions and a temperature between 10°C and 30°C.

The investigation begins when a tool reports an impossible 99°C. Before changing the prompt, inspect the value returned by the tool. If the input is wrong, a polished model answer can still be wrong.

**Working habit:** INHERIT → INVESTIGATE → MODIFY → BREAK → DIAGNOSE → FIX → DEFEND.

## M02-02 Prerequisites and inheritance

Complete Mission 01's baseline first. Then open `lab/mission-02/02_add_tools.py` on the Mission 02 branch. Find the `@tool` decorator, the `location` argument, and `tools=[get_weather]` in the Agent constructor. The Azure configuration is inherited; keep your local `.env` private.

## M02-03 Architecture

User question → Agent → tool schema → get_weather(location) → synthetic result → Agent response.

## M02-04 Core concepts

- **@tool:** Decorator exposing a Python callable to the Agent Framework.
- **Tool schema:** Callable name and argument contract supplied to the Agent.
- **Tool execution:** Python code runs after the Agent chooses a tool invocation.
- **Synthetic result:** Sample data generated locally, not live weather observations.
- **Regression:** Repeatable check guarding against a previously observed defect.

## M02-05 Code-to-concept map

- `lab/mission-02/02_add_tools.py`: read `get_weather()`, the argument schema, and the Agent's tool registration.
- `UPSTREAM.md`: check the upstream Agent Framework provenance.

Notice that `get_weather()` is a random local function. There is no weather provider or external weather API in this sample.

## M02-06 Execution lifecycle

Declare tool and argument schema → register it on Agent → ask question → inspect whether tool was invoked → inspect raw tool output → evaluate final response.

## M02-07 Controlled defect and diagnosis

**BUG-001:** the mission's controlled history includes a bad 99°C result. The current checked sample generates values from 10°C to 30°C, along with a random condition. Neither value is a real forecast.

When you investigate, compare the raw tool output with the Agent's final wording. If the tool supplied 99°C, fix the tool boundary first. A better prompt cannot turn fabricated data into a trustworthy weather report.

Use the investigation sequence: ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN.

## M02-08 Hands-on verification

1. Inspect @tool get_weather(location) and Agent tools=[get_weather].
2. Run the tool locally multiple times; observe random synthetic output.
3. Inspect branch history for BUG-001 if the historical commit is available.
4. Run the Agent against Foundry separately; observe tool invocation rather than assuming it occurred.

## M02-09 Troubleshooting

| Symptom | Inspect |
|---|---|
| Unrealistic weather | Tool code and synthetic random values |
| Tool not invoked | Agent registration, prompt and trace |
| Model response differs | Raw tool output vs generated prose |

## M02-10 Evidence and scope limits

Run the Python tool directly to see its random output, then run the Agent against Foundry and inspect whether the tool was actually called. Those are different observations. The current file supports the corrected range; a full live tool-call trace still needs to be captured by the learner.

## M02-11 Interview defense

**Q1. Is get_weather a real weather API?**

No. It returns randomly selected conditions and temperatures.

**Q2. Why can a model answer be wrong even with a tool?**

The tool may supply bad data or the model may misinterpret its result.

**Q3. Where is the tool registered?**

The Agent constructor receives tools=[get_weather].

**Q4. Why distinguish local tests and Foundry integration?**

Local Python behavior does not prove the model invoked the tool.

## M02-12 Glossary

- **@tool:** Decorator exposing a Python callable to the Agent Framework.
- **Tool schema:** Callable name and argument contract supplied to the Agent.
- **Tool execution:** Python code runs after the Agent chooses a tool invocation.
- **Synthetic result:** Sample data generated locally, not live weather observations.
- **Regression:** Repeatable check guarding against a previously observed defect.

## M02-13 Review checklist

- [ ] Explain the business story and architectural boundary.
- [ ] Locate the relevant source file(s).
- [ ] Demonstrate the healthy baseline.
- [ ] Reproduce or reason about the controlled defect accurately.
- [ ] Run applicable offline tests.
- [ ] Record live integration evidence where applicable.
- [ ] Describe security and persistence limitations.
- [ ] Explain the repair and regression to another engineer.

## M02-14 Maintenance and references

**Primary sources:** `lab/mission-02/02_add_tools.py`, `UPSTREAM.md`.

**Maintenance:** keep these stable section IDs; update behavior descriptions when code changes; never invent successful test results. Log meaningful revisions.

| Date | Version | Change |
|---|---|---|
| 2026-10-30 | 1.0 | Initial living reference created from available repository source |
| 2026-10-30 | 1.1 | Humanized learning narrative and evidence guidance; preserved branch and source links |
