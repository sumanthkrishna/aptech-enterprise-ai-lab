# Setup

## Prerequisites

- Python 3.10+
- Azure CLI authenticated to an account that can access the configured Microsoft Foundry project
- A Microsoft Foundry project endpoint

## Install

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
az login
```

The pinned upstream get-started documentation specifies `agent-framework-foundry` for these samples.

## Configure the pilot samples

The current upstream samples contain placeholder values for:

- project endpoint
- model

For the pilot, learners should replace/configure these only as directed by the instructor. Never commit credentials or secrets.

## Verify

Run Mission 01:

```bash
python lab/mission-01/01_hello_agent.py
```

Then continue only after the baseline works.
