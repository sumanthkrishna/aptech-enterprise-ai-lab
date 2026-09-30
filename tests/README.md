# Tests

Pilot tests will validate:

- clean baseline starts correctly;
- tool behavior can be checked independently;
- session-isolation regression scenarios;
- seeded defects can be reproduced and reset.

Do not add tests that reveal instructor solutions to learners.


## Mission 02 regression

Run:

```bash
python tests/test_mission02_tool.py
```

This validates the local weather source independently of Azure and the model. The end-to-end Mission 02 run is still required as a separate integration check.
