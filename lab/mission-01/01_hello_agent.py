# Copyright (c) Microsoft. All rights reserved.
# Adapted for the Aptech Enterprise AI Lab.
# Upstream: microsoft/agent-framework @ 2c46deb91e70ea6d7bbc99263147e0f470d52546

import asyncio
import sys
from pathlib import Path

# Direct execution sets sys.path to this mission folder. Add the repository root
# so the shared lab package resolves from either the repo root or mission folder.
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from azure.identity import AzureCliCredential

from lab.common.config import get_foundry_config

"""
Hello Agent — Simplest possible agent

This sample creates a minimal agent using FoundryChatClient via a
Microsoft Foundry project endpoint, and runs it in both non-streaming and streaming modes.
"""


async def main() -> None:
    project_endpoint, model = get_foundry_config()

    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model,
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    result = await agent.run("What is the capital of France?")
    print(f"Agent: {result}")

    print("Agent (streaming): ", end="", flush=True)
    async for chunk in agent.run("Tell me a one-sentence fun fact.", stream=True):
        if chunk.text:
            print(chunk.text, end="", flush=True)
    print()


if __name__ == "__main__":
    asyncio.run(main())
