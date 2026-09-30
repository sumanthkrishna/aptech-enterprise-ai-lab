"""Shared configuration for the Aptech Enterprise AI Lab pilot."""

import os

from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "gpt-4o"


def _is_project_endpoint(endpoint: str) -> bool:
    """Return True for a Foundry project endpoint, not a Responses API URL."""
    normalized = endpoint.rstrip("/")
    return (
        bool(normalized)
        and "your-project" not in normalized
        and "/api/projects/" in normalized
        and "/openai/" not in normalized
        and not normalized.endswith("/responses")
    )


def get_foundry_config() -> tuple[str, str]:
    """Return validated Microsoft Foundry project endpoint and model deployment."""
    endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT", "").strip().rstrip("/")
    model = os.getenv("FOUNDRY_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL

    if not endpoint:
        raise RuntimeError(
            "FOUNDRY_PROJECT_ENDPOINT is not configured. "
            "Copy .env.example to .env and set your Microsoft Foundry project endpoint."
        )

    if not _is_project_endpoint(endpoint):
        raise RuntimeError(
            "FOUNDRY_PROJECT_ENDPOINT must be the Foundry PROJECT endpoint, for example "
            "'https://<resource>.services.ai.azure.com/api/projects/<project>'. "
            "Do not use the '/openai/v1/responses' endpoint."
        )

    return endpoint, model
