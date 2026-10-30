# Milestone 02 — Trace the Source of Truth

## Purpose

Milestone 02 turns the clean Mission 02 tool-calling sample into an evidence-driven engineering investigation.

The learner inherits a working agent, observes the boundary between model reasoning and application code, investigates a deliberately incorrect tool result, fixes the component that owns the bad value, and proves the repair with a regression check.

## Learning outcomes

By the end of this milestone, the learner should be able to:

- explain the path from user request to final agent response;
- distinguish model behavior from deterministic application behavior;
- inspect tool registration, schema, arguments, execution, and returned data;
- use runtime evidence before forming a root-cause conclusion;
- apply a minimal source-level repair;
- independently test a tool source without requiring a model call;
- distinguish a fix from a verified fix.

## Investigation loop

**ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**

### ASK

What exactly is wrong? Is the suspicious value created by the model, by the tool, or somewhere else?

### HYPOTHESIZE

Create multiple plausible explanations before editing code.

Examples:

- the model invented the value;
- the wrong tool was selected;
- the correct tool received the wrong argument;
- the tool itself returned bad data;
- the model altered a correct tool result.

### INSPECT

Inspect the agent instructions, tool registration, parameter description, Python source, and learner-visible trace.

### TEST

Run the same scenario and compare:

1. tool argument;
2. raw tool result;
3. final agent response.

### PROVE

Identify the earliest point at which the incorrect value exists.

### EXPLAIN

State the root cause, why competing hypotheses were rejected, what changed, and what evidence proves the repair.

## Healthy path

```text
User: "What's the weather like in Seattle?"
            |
            v
WeatherAgent
            |
            v
Model selects get_weather(location="Seattle")
            |
            v
Python get_weather tool
            |
            v
generate_weather_result("Seattle")
            |
            v
Raw tool result
            |
            v
Model receives tool result
            |
            v
Final natural-language answer
```

The `[TRACE]` output exposes the application boundary so the learner can compare the raw tool result with the final answer.

## Controlled incident — BUG-001

The seeded incident makes the local weather source produce an unmistakably invalid sample value. The intended lesson is not the particular number. The lesson is the diagnostic method:

> Do not blame the model first. Trace the source of truth.

The defect is preserved in Git history rather than left in the final clean branch state.

## Repair strategy

The repair belongs at the component that owns the invalid value. Changing the model, prompt, or final wording would only mask the source defect.

The final implementation also separates `generate_weather_result()` from the decorated agent tool. This makes the application source independently testable without Azure authentication or a model invocation.

## Regression verification

Run the local regression:

```powershell
python tests/test_mission02_tool.py
```

Expected:

```text
[PASS] Mission 02 tool regression: 25 results stayed within the 10–30°C sample contract.
```

Then verify the complete agent path:

```powershell
python lab/mission-02/02_add_tools.py
```

Check that:

- `[TRACE]` shows Seattle as the tool argument;
- the raw tool result contains a high in the sample's 10–30°C contract;
- the final agent response is consistent with the tool result.

## What this milestone proves

It proves that the learner can investigate a simple model/tool boundary, identify the source of a bad value, repair it, and regression-test the local source.

It does **not** prove production weather accuracy, external API reliability, distributed tracing, durable telemetry, or production approval/security design.

## Anticipated issues and reasoning path

| Symptom | Likely category | First evidence to inspect | Appropriate response |
|---|---|---|---|
| No `[TRACE]` output | Tool selection/execution | Agent instructions and tool registration | Prove whether the tool ran before editing it |
| Wrong location in trace | Argument selection/schema | Parameter description and traced argument | Inspect schema/instructions and prompt |
| Correct argument, bad raw value | Tool/source | `tool_result` trace and source function | Fix source-of-truth component |
| Correct raw value, wrong final answer | Model interpretation | Raw result vs final answer | Investigate prompt/model behavior |
| Exception inside tool | Application runtime | Python traceback | Fix tool error; do not classify as hallucination |
| Azure/auth error before tool execution | Environment | verifier / Azure CLI | Restore environment before mission debugging |
| Regression passes but agent run fails | Integration | Foundry/auth/model/tool registration | Separate unit/source evidence from integration evidence |
| Agent wording varies | Nondeterminism | Compare facts, not exact sentence | Verify behavioral contract, not wording |

## Completion evidence

A learner submission should contain:

1. symptom;
2. at least two hypotheses;
3. evidence inspected;
4. raw tool argument/result;
5. root cause;
6. minimal fix;
7. local regression result;
8. end-to-end rerun result;
9. remaining uncertainty.

## Milestone gate

**PASS** requires evidence for both the source-level regression and the complete agent path. A plausible final answer alone is not sufficient.

## Next milestone

After this milestone is stable, proceed to BUG-002 around Mission 03 session reuse and user isolation. Do not expand to Mission 04 before the pilot mechanics are proven.
