# BUG-001 — Incorrect Tool Result

## Learner symptom

The assistant confidently reports an impossible or clearly incorrect tool result.

## Learning objective

Do not blame the model first. Trace the source of truth.

## Investigation evidence

Learner must record symptom, hypothesis, evidence, root cause, fix, and a regression check.

## Injection

Instructor changes the deterministic/tool-return behavior in the Mission 02 lab so the returned value is unmistakably incorrect.

Do not leave the injected defect on the clean baseline.
