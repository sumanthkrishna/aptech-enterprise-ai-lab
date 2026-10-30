# Reproducible Pilot Setup

The lab shares its Foundry configuration across the initial Agent missions. New learners should start from `release/starter-v1`; use `main` for the cumulative implementation after the mission PRs merge.

## 1. Prerequisites

- Python 3.10+
- Azure CLI
- access to a Microsoft Foundry project and deployed model

## 2. Clone and create an isolated environment

```bash
git clone https://github.com/sumanthkrishna/aptech-enterprise-ai-lab.git
cd aptech-enterprise-ai-lab
git switch release/starter-v1

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
FOUNDRY_PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
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
```

Expected behavioral checks:

1. Mission 01 returns a normal response and then a streamed response.
2. For Missions 02 and 03, switch to the matching mission branch and follow its living reference. Those samples are not part of the frozen starter checkpoint.

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

## Learning branches and complete application

Read [START-HERE.md](../../START-HERE.md) for the branch map and personal practice workflow. Mission 04 and 05 add API and RAG capabilities; their offline tests and live Foundry checks are separate gates.
