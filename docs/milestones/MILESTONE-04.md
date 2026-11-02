# Milestone 04 — Turn Your Agent into an API

**Inherited baseline:** mission03-session-isolation (not main).
**Mission:** expose a reusable FastAPI boundary around the existing Foundry
Agent and SessionRouter. **No runtime verification is claimed yet.**

Learning loop: INHERIT → INVESTIGATE → MODIFY → BREAK (hypothesis) → FIX →
DEFEND. BUG-003 is a proposed global-session routing failure to reproduce
in a controlled exercise, not a defect currently present in the repaired code.

Acceptance: offline contract and session tests, live Foundry run, explain
422 validation and 502 backend error, distinguish completed-answer SSE from
real model token streaming, and state authentication/multiworker limitations.

See lab/mission-04/README.md and the separate downloadable self-learning guide.
