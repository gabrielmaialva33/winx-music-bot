import asyncio
import sys

from pyrogram import Client

import config
from ..logging import LOGGER

assistants = []
assistant_ids = []


class Userbot(Client):
    def __init__(self):
        self.clients: list[Client] = []
        session_strings = config.STRING_SESSIONS

        for i, session in enumerate(session_strings, start=1):
            client = Client(
                f"WinxString{i}",
                api_id=config.API_ID,
                api_hash=config.API_HASH,
                in_memory=True,
                session_string=session.strip(),
            )
            self.clients.append(client)

    async def _start(self, client, index):
        LOGGER(__name__).info("Starting Assistant Clients")
        try:
            await client.start()
            assistants.append(index)
            await client.send_message(config.LOG_GROUP_ID, "Assistant Started")

            get_me = await client.get_me()
            client.username = get_me.username
            client.id = get_me.id
            client.mention = get_me.mention
            assistant_ids.append(get_me.id)
            client.name = f"{get_me.first_name} {get_me.last_name or ''}".strip()

            await client.join_chat("@cinewinx")
            await client.join_chat("@cinewinxcoments")

        except Exception as e:
            LOGGER(__name__).error(
                f"Assistant Account {index} failed with error: {str(e)}."
            )
            sys.exit(1)

    async def start(self):
        tasks = []  # List to hold start tasks
        for i, client in enumerate(self.clients, start=1):
            task = self._start(client, i)
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def stop(self):
        """Gracefully stop all clients."""
        tasks = [client.stop() for client in self.clients]
        await asyncio.gather(*tasks)
