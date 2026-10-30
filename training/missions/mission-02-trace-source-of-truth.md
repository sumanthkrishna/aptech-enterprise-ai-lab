# Mission 02 — Trace the Source of Truth

## Scenario

You inherited a weather agent. The assistant gives a confident answer, but the reported value looks suspicious. Your job is not to rewrite the agent or change the model. Your job is to determine where the value came from and prove the root cause.

## Method

**ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**

An AI-generated answer is not evidence.

## Investigation questions

1. Where is the tool defined?
2. How is the tool registered with the agent?
3. What description/schema can the model see?
4. What arguments are supplied to the tool?
5. What value does the Python tool produce before the model sees it?
6. Does the final agent answer preserve, alter, or contradict that value?
7. Which component owns the incorrect value?

## Run

```powershell
python lab/mission-02/02_add_tools.py
```

The mission prints learner-visible `[TRACE]` lines. Treat them as evidence from the application boundary, not as decoration.

## Evidence worksheet

Record:

| Field | Your evidence |
|---|---|
| Symptom | |
| Initial hypothesis | |
| Code/config inspected | |
| Tool arguments observed | |
| Raw tool result observed | |
| Agent result observed | |
| Root cause | |
| Fix | |
| Regression evidence | |
| Remaining uncertainty | |

## Rules

- Do not blame the model without evidence.
- Do not change the model merely to make the symptom disappear.
- Do not accept a plausible final sentence as proof of correct tool execution.
- Prefer the smallest fix at the component that owns the faulty value.
- After the fix, run a regression check.

## Completion gate

You are done only when you can explain the full path:

`User request → Agent → tool selection → arguments → Python tool → tool result → model → final answer`

and support your root-cause claim with observed evidence.
