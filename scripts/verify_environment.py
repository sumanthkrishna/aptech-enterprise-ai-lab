"""Verify local prerequisites before running the Aptech AI Lab pilot."""

import importlib.util
import os
import shutil
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

checks: list[tuple[str, bool, str]] = []

checks.append(("Python 3.10+", sys.version_info >= (3, 10), sys.version.split()[0]))
checks.append(("Azure CLI installed", shutil.which("az") is not None, shutil.which("az") or "not found"))

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

print("Aptech Enterprise AI Lab — Environment Verification\n")
failed = False
for name, ok, detail in checks:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    failed = failed or not ok

if failed:
    print("\nEnvironment is NOT ready. See docs/setup/README.md.")
    raise SystemExit(1)

print("\nStatic environment checks passed.")
print("Next: run 'az account show' to confirm Azure CLI authentication, then run Mission 01.")
