"""Shared configuration for the Aptech Enterprise AI Lab pilot."""

import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gpt-4o"


def get_foundry_config() -> tuple[str, str]:
    """Return validated Microsoft Foundry endpoint and model configuration."""
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip()
    model = os.getenv("FOUNDRY_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL

    if not endpoint:
        raise RuntimeError(
            "FOUNDRY_PROJECT_ENDPOINT is not configured. "
            "Copy .env.example to .env and set your Microsoft Foundry project endpoint."
        )

    if "your-project" in endpoint:
        raise RuntimeError(
            "FOUNDRY_PROJECT_ENDPOINT still contains the example placeholder. "
            "Set it to a real Microsoft Foundry project endpoint."
        )

    return endpoint, model
