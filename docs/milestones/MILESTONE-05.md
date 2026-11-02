# Milestone 05 — Ground the Agent in Documents (RAG)

Created from mission04-fastapi-agent-service. Preserve M01–M04.

**Story:** Support assistant must answer from approved synthetic policies.
**Workflow:** load JSON → section chunks → lexical overlap search → active
metadata filter → context prompt → inherited Agent → response + source IDs.

**BUG-004:** retired REMOTE-2025 is included when active_only=False.
The repaired path filters inactive documents before ranking.

**Evidence:** offline retrieval tests, FastAPI contract tests, Alice/Bob
session isolation, and separate live Foundry integration.

**Limits:** no embeddings, vector DB, PDF ingestion, claim-level citation
validation, authentication, durable memory, or verified production security.
Do not merge before runtime evidence and review.
