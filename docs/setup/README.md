# Reproducible Pilot Setup

The v0.1 pilot uses one shared configuration for Missions 01–03.

## 1. Prerequisites

- Python 3.10+
- Azure CLI
- access to a Microsoft Foundry project and deployed model

## 2. Clone and create an isolated environment

```bash
git clone https://github.com/sumanthkrishna/aptech-enterprise-ai-lab.git
cd aptech-enterprise-ai-lab

python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configure

Copy the template:

**Windows PowerShell**

```powershell
Copy-Item .env.example .env
```

**macOS/Linux**

```bash
cp .env.example .env
```

Edit `.env`:

```text
FOUNDRY_PROJECT_ENDPOINT=https://<your-project>.services.ai.azure.com
FOUNDRY_MODEL=gpt-4o
```

Do not commit `.env`. It is ignored by Git.

## 4. Authenticate

```bash
az login
az account show
```

The samples use `AzureCliCredential`; no Azure credential is stored in this repository.

## 5. Verify the environment

Run from the repository root:

```bash
python scripts/verify_environment.py
```

All static checks should show PASS.

## 6. Run the clean baseline

Always run from the repository root so the shared `lab` package resolves consistently:

```bash
python lab/mission-01/01_hello_agent.py
python lab/mission-02/02_add_tools.py
python lab/mission-03/03_multi_turn.py
```

Expected behavioral checks:

1. Mission 01 returns a normal response and then a streamed response.
2. Mission 02 answers the Seattle weather question by using the sample tool.
3. Mission 03's second turn recalls the fictional name/hobby because the same session is reused.

Exact model wording is nondeterministic; validate behavior, not sentence-for-sentence output.

## 7. Troubleshooting boundary

If verification fails, fix setup before starting a mission. Do not turn environment/configuration failures into accidental learner exercises.

See `docs/troubleshooting/README.md`.

## Configuration design

Missions 01–03 use `lab/common/config.py` to resolve:

- `FOUNDRY_PROJECT_ENDPOINT`
- `FOUNDRY_MODEL`

The endpoint is mandatory. The model defaults to `gpt-4o` if omitted.

This removes machine-specific endpoint edits from the mission source and gives every learner the same setup path.
