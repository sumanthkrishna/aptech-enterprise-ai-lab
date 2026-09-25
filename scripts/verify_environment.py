"""Verify local prerequisites and Azure authentication for the Aptech AI Lab."""

import importlib.util
import json
import os
import shutil
import subprocess
import sys

from dotenv import load_dotenv

load_dotenv()

checks: list[tuple[str, bool, str]] = []

checks.append(("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0]))
az = shutil.which("az")
checks.append(("Azure CLI installed", az is not None, az or "not found"))

for package in ("agent_framework", "azure.identity", "dotenv"):
    checks.append((f"Python package: {package}", importlib.util.find_spec(package) is not None, package))

endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip()
checks.append(
    (
        "FOUNDRY_PROJECT_ENDPOINT configured",
        bool(endpoint) and "your-project" not in endpoint,
        endpoint if endpoint else "missing",
    )
)

model = os.getenv("FOUNDRY_MODEL", "gpt-4o").strip() or "gpt-4o"
checks.append(("FOUNDRY_MODEL resolved", bool(model), model))

if az:
    try:
        proc = subprocess.run(
            [az, "account", "show", "--output", "json"],
            check=True,
            capture_output=True,
            text=True,
            timeout=20,
        )
        account = json.loads(proc.stdout)
        detail = f"{account.get('name', 'unknown subscription')} / tenant {account.get('tenantId', 'unknown')}"
        checks.append(("Azure CLI authenticated", True, detail))
    except Exception:
        checks.append(("Azure CLI authenticated", False, "run: az login"))

print("Aptech Enterprise AI Lab — Environment Verification\n")
failed = False
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    failed = failed or not ok

if failed:
    print("\nEnvironment is NOT ready. See docs/setup/README.md.")
    raise SystemExit(1)

print("\nEnvironment checks passed.")
print("Next: python lab/mission-01/01_hello_agent.py")
