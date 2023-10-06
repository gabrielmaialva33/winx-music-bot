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
                        BotCommand("write", "Escreve um texto em uma imagem"),
                        BotCommand("webss", "Tira uma captura de tela de um site"),
                        BotCommand("cuddle", "Envia um comando de carinho"),
                        BotCommand("shrug", "Envia um comando de dar de ombros"),
                        BotCommand("poke", "Envia um comando de cutucar"),
                        BotCommand("facepalm", "Envia um comando de facepalm"),
                        BotCommand("stare", "Envia um comando de olhar fixamente"),
                        BotCommand("pout", "Envia um comando de fazer bico"),
                        BotCommand("handhold", "Envia um comando de segurar a mão"),
                        BotCommand("wave", "Envia um comando de acenar"),
                        BotCommand("blush", "Envia um comando de corar"),
                        BotCommand("neko", "Envia um comando neko"),
                        BotCommand("dance", "Envia um comando de dançar"),
                        BotCommand("baka", "Envia um comando de insulto leve"),
                        BotCommand("bore", "Envia um comando de tédio"),
                        BotCommand("laugh", "Envia um comando de risada"),
                        BotCommand("smug", "Envia um comando de arrogância"),
                        BotCommand("thumbsup", "Envia um comando de joinha"),
                        BotCommand("shoot", "Envia um comando de atirar"),
                        BotCommand("tickle", "Envia um comando de cócegas"),
                        BotCommand("feed", "Envia um comando de alimentar"),
                        BotCommand("think", "Envia um comando de pensar"),
                        BotCommand("wink", "Envia um comando de piscar"),
                        BotCommand("sleep", "Envia um comando de dormir"),
                        BotCommand("punch", "Envia um comando de soco"),
                        BotCommand("cry", "Envia um comando de chorar"),
                        BotCommand("kill", "Envia um comando de matar"),
                        BotCommand("smile", "Envia um comando de sorrir"),
                        BotCommand("highfive", "Envia um comando de toca aqui"),
                        BotCommand("slap", "Envia um comando de tapa"),
                        BotCommand("hug", "Envia um comando de abraço"),
                        BotCommand("pat", "Envia um comando de afagar"),
                        BotCommand("waifu", "Envia um comando waifu"),
                        BotCommand("couple", "Envia um comando de casal do dia")
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
