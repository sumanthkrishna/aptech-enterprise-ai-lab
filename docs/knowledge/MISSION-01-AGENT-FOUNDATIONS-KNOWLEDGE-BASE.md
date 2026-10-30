---
title: "Mission 01 – Know Your System"
project: "Aptech Enterprise AI Lab"
mission: "01"
version: "1.1"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-01, self-learning]
---

# Mission 01 – Know Your System

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Mission navigation and branch provenance

**Documentation home:** [Living Knowledge Library](./README.md) (maintained on `mission05-rag-grounded-answers`).  
**Mission implementation branch:** [`main`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/tree/main).  
**Verified entry point:** [`lab/mission-01/01_hello_agent.py`](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/main/lab/mission-01/01_hello_agent.py).  
**Learning sequence:** Start of curriculum · [Mission 02 →](./MISSION-02-AGENT-TOOLS-KNOWLEDGE-BASE.md).

**Version-control note:** Mission 01's baseline is on `main`, not a separate `mission01-*` branch. Mission 02–05 have individual branches. These knowledge documents are consolidated on the Mission 05 branch and link to each mission's implementation branch; they have **not** been copied into every earlier branch. No merges are performed by documentation updates.


## Retrieval index

| ID | Topic |
|---|---|
| [M01-01](#m01-01-story-and-outcome) | Story and outcome |
| [M01-02](#m01-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M01-03](#m01-03-architecture) | Architecture |
| [M01-04](#m01-04-core-concepts) | Core concepts |
| [M01-05](#m01-05-code-to-concept-map) | Code-to-concept map |
| [M01-06](#m01-06-execution-lifecycle) | Execution lifecycle |
| [M01-07](#m01-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M01-08](#m01-08-hands-on-verification) | Hands-on verification |
| [M01-09](#m01-09-troubleshooting) | Troubleshooting |
| [M01-10](#m01-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M01-11](#m01-11-interview-defense) | Interview defense |
| [M01-12](#m01-12-glossary) | Glossary |
| [M01-13](#m01-13-review-checklist) | Review checklist |
| [M01-14](#m01-14-maintenance-and-references) | Maintenance and references |

## M01-01 Story and outcome

You've inherited a small Foundry Agent sample. It answers a question, but before you add tools or sessions, you need to know exactly what starts it, where the model is configured, and what a successful run proves. Your first job is to trace the request from the local script to Foundry and back.

**Your assignment:** explain the baseline in your own words, run it, and save the actual output. A green environment check is useful, but it doesn't prove the Agent made a successful model call.

**Working habit:** INHERIT → INVESTIGATE → MODIFY → BREAK → DIAGNOSE → FIX → DEFEND.

## M01-02 Prerequisites and inheritance

Start with `lab/mission-01/01_hello_agent.py`. Create a Python virtual environment, install the repository requirements, and check `lab/common/config.py`. Set the Foundry project endpoint and deployment in your local `.env`; keep credentials and that file out of Git. This is the starting mission, so there is no earlier lab to inherit.

## M01-03 Architecture

Configuration → FoundryChatClient → Agent(instructions) → run → response.

## M01-04 Core concepts

- **Agent:** An application object that combines model client, instructions and execution.
- **FoundryChatClient:** Agent Framework integration to a Microsoft Foundry project.
- **AzureCliCredential:** Azure identity credential sourced from Azure CLI login context.
- **Project endpoint:** Foundry URL containing /api/projects/, distinct from an /openai/... responses URL.
- **Deployment:** Configured model deployment name, distinct from an endpoint.

## M01-05 Code-to-concept map

- `lab/mission-01/01_hello_agent.py`: follow `get_foundry_config()`, client construction, Agent construction, `agent.run()`, and the streaming loop.
- `lab/common/config.py`: see how the project endpoint and model name are validated.
- `scripts/verify_environment.py`: understand what the environment check actually tests.
- `UPSTREAM.md`: identify the Microsoft Agent Framework source used by the lab.
- `README.md`: find the repository's learning structure.

## M01-06 Execution lifecycle

Validate project endpoint and deployment → authenticate Azure CLI → construct client → construct Agent → invoke → inspect actual result.

## M01-07 Controlled defect and diagnosis

There is no numbered defect to repair yet. Treat configuration mistakes as your first investigation: a Responses API URL supplied as a Foundry *project* endpoint, a missing deployment, or an expired Azure CLI login can stop the sample before you learn anything about Agent behavior.

Start with the earliest failing boundary. Check configuration first, then authentication, then the Agent call. Don't attribute every failure to the model.

Use the investigation sequence: ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN.

## M01-08 Hands-on verification

1. Inspect lab/mission-01/01_hello_agent.py and its non-streaming and streaming Agent.run calls.
2. Check .env configuration without committing secrets.
3. Run python scripts/verify_environment.py.
4. Run python lab/mission-01/01_hello_agent.py against Foundry and retain output; do not infer live success from configuration alone.

## M01-09 Troubleshooting

| Symptom | Inspect |
|---|---|
| Invalid endpoint | Foundry project path vs /openai/ path |
| Credential error | Azure CLI login and permissions |
| Deployment failure | FOUNDRY_MODEL and deployment access |

## M01-10 Evidence and scope limits

Read the source, then run it. The script demonstrates both a regular Agent call and a streamed response. Keep the terminal output and note which mode you observed. An environment check only establishes local prerequisites; it does not prove the Foundry request completed. This reference does not claim a new live run.

## M01-11 Interview defense

**Q1. Why establish a baseline?**

Without a known working reference, later failures cannot be attributed confidently to your changes.

**Q2. What is a Foundry project endpoint?**

The configuration validator expects a path containing /api/projects/ and rejects /openai/ responses-style paths.

**Q3. Does a configured model prove a successful call?**

No. Authentication, deployment access, network and runtime must be exercised separately.

**Q4. What is an Agent versus a model?**

The model generates responses; the Agent application defines how the model is invoked and what instructions and capabilities are supplied.

## M01-12 Glossary

- **Agent:** An application object that combines model client, instructions and execution.
- **FoundryChatClient:** Agent Framework integration to a Microsoft Foundry project.
- **AzureCliCredential:** Azure identity credential sourced from Azure CLI login context.
- **Project endpoint:** Foundry URL containing /api/projects/, distinct from an /openai/... responses URL.
- **Deployment:** Configured model deployment name, distinct from an endpoint.

## M01-13 Review checklist

- [ ] Explain the business story and architectural boundary.
- [ ] Locate the relevant source file(s).
- [ ] Demonstrate the healthy baseline.
- [ ] Reproduce or reason about the controlled defect accurately.
- [ ] Run applicable offline tests.
- [ ] Record live integration evidence where applicable.
- [ ] Describe security and persistence limitations.
- [ ] Explain the repair and regression to another engineer.

## M01-14 Maintenance and references

**Primary sources:** `lab/common/config.py`, `scripts/verify_environment.py`, `UPSTREAM.md`, `README.md`.

**Maintenance:** keep these stable section IDs; update behavior descriptions when code changes; never invent successful test results. Log meaningful revisions.

| Date | Version | Change |
|---|---|---|
| 2026-10-30 | 1.0 | Initial living reference created from available repository source |
| 2026-10-30 | 1.1 | Humanized learning narrative and evidence guidance; preserved branch and source links |
