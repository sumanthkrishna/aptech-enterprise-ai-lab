---
title: "Mission 01 — Know Your System"
project: "Aptech Enterprise AI Lab"
mission: "01"
version: "1.0"
updated: "2026-10-30"
status: "Living reference; runtime evidence separately required"
tags: [enterprise-ai, mission-01, self-learning]
---

# Mission 01 — Know Your System

> **Navigation:** [Curriculum index](./README.md) · [Mission 05 RAG](./MISSION-05-RAG-KNOWLEDGE-BASE.md)

## Retrieval index

| ID | Topic |
|---|---|
| [M01-01](#m01-01-story-and-outcome) | Story and outcome |
| [M01-02](#m01-02-prerequisites-and-inheritance) | Prerequisites and inheritance |
| [M01-03](#m01-03-architecture) | Architecture |
| [M01-04](#m01-04-core-concepts) | Core concepts |
| [M01-05](#m01-05-codetoconcept-map) | Code-to-concept map |
| [M01-06](#m01-06-execution-lifecycle) | Execution lifecycle |
| [M01-07](#m01-07-controlled-defect-and-diagnosis) | Controlled defect and diagnosis |
| [M01-08](#m01-08-handson-verification) | Hands-on verification |
| [M01-09](#m01-09-troubleshooting) | Troubleshooting |
| [M01-10](#m01-10-evidence-and-scope-limits) | Evidence and scope limits |
| [M01-11](#m01-11-interview-defense) | Interview defense |
| [M01-12](#m01-12-glossary) | Glossary |
| [M01-13](#m01-13-review-checklist) | Review checklist |
| [M01-14](#m01-14-maintenance-and-references) | Maintenance and references |

## M01-01 Story and outcome

A new engineer inherits an Azure Foundry Agent and must identify each component and prove the baseline before modifying it.

**Goal:** inherit → investigate → modify → break or model failure → diagnose → fix → defend. Do not confuse a passing offline check with a live Foundry integration result.

## M01-02 Prerequisites and inheritance

Read the earlier mission references before this one. Use a Python virtual environment, install repository requirements, and configure Microsoft Foundry only when running live Agent examples. Never commit .env secrets. This mission builds on the prior one rather than replacing it.

## M01-03 Architecture

Configuration → FoundryChatClient → Agent(instructions) → run → response.

## M01-04 Core concepts

- **Agent:** An application object that combines model client, instructions and execution.
- **FoundryChatClient:** Agent Framework integration to a Microsoft Foundry project.
- **AzureCliCredential:** Azure identity credential sourced from Azure CLI login context.
- **Project endpoint:** Foundry URL containing /api/projects/, distinct from an /openai/... responses URL.
- **Deployment:** Configured model deployment name, distinct from an endpoint.

## M01-05 Code-to-concept map

- `lab/common/config.py` — inspect for the concept and verify its behavior.
- `scripts/verify_environment.py` — inspect for the concept and verify its behavior.
- `UPSTREAM.md` — inspect for the concept and verify its behavior.
- `README.md` — inspect for the concept and verify its behavior.

## M01-06 Execution lifecycle

Validate project endpoint and deployment → authenticate Azure CLI → construct client → construct Agent → invoke → inspect actual result.

## M01-07 Controlled defect and diagnosis

No numbered defect in this mission; the exercise is configuration and baseline investigation.

**Diagnostic method:** ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN. State the earliest incorrect boundary; do not substitute a confident Agent answer for evidence.

## M01-08 Hands-on verification

1. Inspect the Mission 01 runnable sample location in the repository (not verified from the available source paths).
2. Check .env configuration without committing secrets.
3. Run python scripts/verify_environment.py.
4. Run the actual Agent sample against Foundry and retain output; do not infer live success from configuration alone.

## M01-09 Troubleshooting

| Symptom | Inspect |
|---|---|
| Invalid endpoint | Foundry project path vs /openai/ path |
| Credential error | Azure CLI login and permissions |
| Deployment failure | FOUNDRY_MODEL and deployment access |

## M01-10 Evidence and scope limits

**Source-supported facts:** the listed repository code and tests describe the behavior above. **Not automatically proven:** live Foundry runtime, production readiness, authentication, durable memory, or a reviewed deployment. Capture actual commands, output, commit SHA and reviewer notes before changing a gate to PASS.

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
