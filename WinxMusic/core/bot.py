#
# Copyright (C) 2021-2022 by mrootx@Github, < https://github.com/gabrielmaialva33 >.
#
# This file is part of < https://github.com/gabrielmaialva33/winx-music-bot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/gabrielmaialva33/winx-music-bot/blob/master/LICENSE >
#
# All rights reserved.

import sys

from pyrogram import Client
from pyrogram.types import BotCommand

import config
from ..logging import LOGGER


class WinxBot(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "WinxMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        try:
            await self.send_message(
                config.LOG_GROUP_ID, "Bot Started"
            )
        except:
            LOGGER(__name__).error(
                "O bot falhou ao acessar o grupo de logs. Certifique-se de ter adicionado seu bot ao seu canal de log "
                "e promovido como administrador! "
            )
            sys.exit()
        try:
            await self.set_bot_commands([
                BotCommand("ping", "Check that bot is alive or dead"),
                BotCommand("play", "Starts playing the requested song"),
                BotCommand("skip", "Moves to the next track in queue"),
                BotCommand("pause", "Pause the current playing song"),
                BotCommand("resume", "Resume the paused song"),
                BotCommand("end", "Clear the queue and leave voice chat"),
                BotCommand("shuffle", "Randomly shuffles the queued playlist."),
                BotCommand("playmode", "Allows you to change the default playmode for your chat"),
                BotCommand("settings", "Open the settings of the music bot for your chat.")])
        except:
            pass
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != "administrator":
            LOGGER(__name__).error(
                "Por favor, promova o Bot como Admin no Grupo de Logs!"
            )
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicBot Started as {self.name}")
