# Copyright (c) Microsoft. All rights reserved.
# Adapted for the Aptech Enterprise AI Lab.
# Upstream: microsoft/agent-framework @ 2c46deb91e70ea6d7bbc99263147e0f470d52546

import asyncio

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

    session = agent.create_session()

    result = await agent.run("My name is Alice and I love hiking.", session=session)
    print(f"Agent: {result}\n")

    result = await agent.run("What do you remember about me?", session=session)
    print(f"Agent: {result}")


if __name__ == "__main__":
    asyncio.run(main())
