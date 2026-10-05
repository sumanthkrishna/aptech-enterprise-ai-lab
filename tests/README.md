# Tests

Pilot tests will validate:

- clean baseline starts correctly;
- tool behavior can be checked independently;
- session-isolation regression scenarios;
- seeded defects can be reproduced and reset.

Do not add tests that reveal instructor solutions to learners.


## Mission 03 regression

Run:

```bash
python tests/test_mission03_session_routing.py
```

This validates the lab's application-level session ownership policy without Azure/model calls. The end-to-end Mission 03 run remains a separate integration check.
