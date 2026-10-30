# Start here: Aptech Enterprise AI Lab

Welcome. You'll learn this lab the way an engineer joins an existing project: run a working sample, understand its boundaries, investigate a failure, and explain your fix.

## Choose your starting point

- **New to the lab?** Check out `release/starter-v1`. It holds the Mission 01 baseline and stays separate from future mission development.
- **Working on a specific exercise?** Open that mission's branch and create your own `learner/<name>-missionXX` branch. The mission branch contains the reference implementation and, where documented, a controlled defect in its history.
- **Want to see the full application?** Once the mission PRs are merged, `main` will hold the cumulative working code for all completed missions. Until then, use the individual mission branches.

The living [knowledge library](https://github.com/sumanthkrishna/aptech-enterprise-ai-lab/blob/mission05-rag-grounded-answers/docs/knowledge/README.md) currently lives on the Mission 05 branch. It links to the right source branch for each mission. After the PRs merge, the same path will be available on `main`.

## Your first session

1. Clone the repository and switch to the starter branch:

   ```bash
   git clone https://github.com/sumanthkrishna/aptech-enterprise-ai-lab.git
   cd aptech-enterprise-ai-lab
   git switch release/starter-v1
   python -m venv .venv
   ```

2. Activate the environment. In PowerShell: `.\.venv\Scripts\Activate.ps1`. On macOS/Linux: `source .venv/bin/activate`.
3. Install packages: `python -m pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`. Set `FOUNDRY_PROJECT_ENDPOINT` to your **project endpoint** containing `/api/projects/<project-name>`, and `FOUNDRY_MODEL` to your deployed model name. Don't use a `/openai/` Responses API URL here. Never commit `.env`.
5. Sign in with `az login`. Run `python scripts/verify_environment.py`.
6. Run `python lab/mission-01/01_hello_agent.py`. Inspect both the regular response and the streaming output.

If a command fails, start with [setup](docs/setup/README.md) and [troubleshooting](docs/troubleshooting/README.md). A passing environment check does not prove a successful live Foundry call.

## Your investigation notebook

For each mission, write down the question you are trying to answer, your hypothesis, the file or trace you inspected, the test you ran, and what the result actually proves. Keep failed hypotheses. They often teach more than the final fix.

Use **ASK → HYPOTHESIZE → INSPECT → TEST → PROVE → EXPLAIN**. An Agent's confident answer is not evidence.

## Mission branches

| Mission | Reference branch | Focus |
|---|---|---|
| 01 | `release/starter-v1` | Baseline Agent and Foundry configuration |
| 02 | `mission02-investigate-tool-path` | Tool source of truth, BUG-001 |
| 03 | `mission03-session-isolation` | Alice/Bob sessions, BUG-002 |
| 04 | `mission04-fastapi-agent-service` | FastAPI, request validation, hypothetical BUG-003 |
| 05 | `mission05-rag-grounded-answers` | Lexical retrieval, retired policies, BUG-004 |

Each mission branch is a reference snapshot, not your personal workspace. Make a new learner branch before experimenting.

## A note about readiness

The lab uses synthetic data. Mission 04's SSE endpoint sends one completed answer rather than model tokens. Mission 05 uses lexical retrieval, not a vector database, and does not independently verify generated citations. Offline tests and live Foundry verification are separate checkpoints.
