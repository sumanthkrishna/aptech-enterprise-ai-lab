# Mission 07 learner card: Who should answer this?

**Inherited system:** an Agent lab with tools, session routing, an API, and a document retrieval exercise. The new orchestration layer is intentionally simple and runs offline.

**Your assignment:** Alice asks about remote-work policy. Bob asks for help debugging an API. Trace how the orchestrator chooses the specialist, what it passes forward, and why a 200 response is not proof that the specialist gave a correct answer.

Follow **ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**.

1. Predict which handler receives each question. Inspect `choose_specialist`.
2. Run `python lab/mission-07/orchestrator.py`. Record request IDs and routing reasons.
3. Read the `Handoff` record. Explain why it is immutable and per request.
4. Investigate BUG-006: what could happen if a global `last_user` variable replaced the explicit handoff? Demonstrate only in a disposable learner branch.
5. Run `python tests/test_mission07_orchestration.py`. Add a test for a question that mixes policy and engineering terms.
6. Review the HTTP contract in `service.py`. Test malformed input and a failing specialist.
7. Explain what you'd need before swapping in real Foundry Agents or the Mission 05 retrieval layer.

**Submit:** a flow diagram, test transcript, root-cause explanation, one additional regression test, and a short technical defense. Don't invent live test results.
