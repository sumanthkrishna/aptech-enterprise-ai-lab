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


async def main() -> None:
    project_endpoint, model = get_foundry_config()

    client = FoundryChatClient(
        project_endpoint=project_endpoint,
        model=model,
        credential=AzureCliCredential(),
    )

    agent = Agent(
        client=client,
        name="ConversationAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    alice_session = agent.create_session()

    print("[TRACE] user=Alice action=create_session")
    result = await agent.run("My name is Alice and I love hiking.", session=alice_session)
    print(f"Agent: {result}\n")

    print("[TRACE] user=Alice action=reuse_same_session")
    result = await agent.run("What do you remember about me?", session=alice_session)
    print(f"Agent: {result}\n")

    # BUG-002 (controlled incident): Bob is incorrectly routed to Alice's session.
    # Synthetic identities only; never use real personal or sensitive information.
    print("[TRACE] user=Bob action=INCORRECTLY_reuse_alice_session")
    result = await agent.run(
        "I am Bob. Before I tell you anything else, what do you remember about me?",
        session=alice_session,
    )
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
