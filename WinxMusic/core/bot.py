#
# Copyright (C) 2021-2023 by Maia, < https://github.com/gabrielmaialva33 >.
#
# This file is part of < https://github.com/gabrielmaialva33/winx-music-bot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/gabrielmaialva33/winx-music-bot/blob/master/LICENSE >
#
# All rights reserved.

import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
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
        get_me = self.me

        self.username = get_me.username
        self.id = get_me.id

        try:
            await self.send_message(
                config.LOG_GROUP_ID, "Bot Started"
            )
        except:
            LOGGER(__name__).error(
                "Bot has failed to access the log Group. Make sure that you have added your bot to your log channel and promoted as admin!"
            )
            sys.exit()
        if config.SET_CMDS == str(True):
            try:
                await self.set_bot_commands(
                    [
                        BotCommand("ping", "Veja se o bot está online"),
                        BotCommand("play", "Reproduz a música solicitada"),
                        BotCommand("skip", "Pula a música atual"),
                        BotCommand("pause", "Pausa a música atual"),
                        BotCommand("resume", "Retoma a música atual"),
                        BotCommand("end", "Para a música atual e limpa a fila"),
                        BotCommand("shuffle", "Embaralha a fila de músicas"),
                        BotCommand("playmode", "Alterna entre os modos de reprodução"),
                        BotCommand("settings", "Abre o menu de configurações"),
                        BotCommand("wifu", "Envia uma imagem aleatória de anime"),
                    ]
                )
            except:
                pass
        else:
            pass
        a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please promote Bot as Admin in Logger Group"
            )
            sys.exit()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"WinxBot Started as: {self.name}")
