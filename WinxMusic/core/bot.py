import asyncio

import uvloop

uvloop.install()

import sys

from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import BotCommand
from pyrogram.types import BotCommandScopeAllChatAdministrators
from pyrogram.types import BotCommandScopeAllGroupChats
from pyrogram.types import BotCommandScopeAllPrivateChats
from pyrogram.types import BotCommandScopeChat
from pyrogram.types import BotCommandScopeChatMember
from pyrogram.errors import ChatSendPhotosForbidden
from pyrogram.errors import ChatWriteForbidden
from pyrogram.errors import FloodWait
from pyrogram.errors import MessageIdInvalid

import config

from ..logging import LOGGER


class WinxBot(Client):
    def __init__(self: "WinxBot"):

        self.username = None
        self.id = None
        self.name = None
        self.mention = None

        LOGGER(__name__).info(f"Starting Bot")
        super().__init__(
            "WinxMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            sleep_threshold=240,
            max_concurrent_transmissions=5,
            workers=50,
        )

    async def edit_message_text(self, *args, **kwargs):
        try:
            return await super().edit_message_text(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.edit_message_text(self, *args, **kwargs)
        except MessageIdInvalid:
            pass

    async def send_message(self, *args, **kwargs):
        if kwargs.get("send_direct", False):
            kwargs.pop("send_direct", None)
            return await super().send_message(*args, **kwargs)

        try:
            return await super().send_message(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.send_message(self, *args, **kwargs)
        except ChatWriteForbidden:
            chat_id = kwargs.get("chat_id") or args[0]
            if chat_id:
                await self.leave_chat(chat_id)

    async def send_photo(self, *args, **kwargs):
        try:
            return await super().send_photo(*args, **kwargs)
        except FloodWait as e:
            time = int(e.value)
            await asyncio.sleep(time)
            if time < 25:
                return await self.send_photo(self, *args, **kwargs)
        except ChatSendPhotosForbidden:
            chat_id = kwargs.get("chat_id") or args[0]
            if chat_id:
                await self.send_message(
                    chat_id,
                    "I don't have the right to send photos in this chat, leaving now..",
                )
                await self.leave_chat(chat_id)

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        self.username = get_me.username
        self.id = get_me.id
        self.name = f"{get_me.first_name} {get_me.last_name or ''}"
        self.mention = get_me.mention

        try:
            await self.send_message(
                config.LOG_GROUP_ID,
                text=f"🚀 <u><b>{self.mention} Bot Iniciado :</b></u>\n\n🆔 <b>ID</b>: <code>{self.id}</code>\n📛 <b>Nome</b>: {self.name}\n🔗 <b>Nome de usuário:</b> @{self.username}",
            )
        except Exception as e:
            LOGGER(__name__).error(
                "Bot failed to access the log group. Ensure the bot is added and promoted as admin."
            )
            LOGGER(__name__).error("Error details:", exc_info=True)
            sys.exit()

        if config.SET_CMDS == str(True):
            try:
                await self._set_default_commands()
            except Exception as e:
                LOGGER(__name__).warning("Failed to set commands:", exc_info=True)

    async def _set_default_commands(self):
        private_commands = [
            BotCommand("start", "Iniciar o bot"),
            BotCommand("help", "Obter o menu de ajuda"),
            BotCommand("ping", "Verificar se o bot está ativo ou inativo"),
        ]
        group_commands = [BotCommand("play", "Começar a tocar a música solicitada")]
        admin_commands = [
            BotCommand("play", "Começar a tocar a música solicitada"),
            BotCommand("skip", "Ir para a próxima música na fila"),
            BotCommand("pause", "Pausar a música atual"),
            BotCommand("resume", "Retomar a música pausada"),
            BotCommand("end", "Limpar a fila e sair do chat de voz"),
            BotCommand("shuffle", "Embaralhar aleatoriamente a playlist na fila"),
            BotCommand("playmode", "Alterar o modo de reprodução padrão do seu chat"),
            BotCommand("settings", "Abrir as configurações do bot para o seu chat"),
        ]
        owner_commands = [
            BotCommand("update", "Atualizar o bot"),
            BotCommand("restart", "Reiniciar o bot"),
            BotCommand("logs", "Obter os registros"),
            BotCommand("export", "Exportar todos os dados do MongoDB"),
            BotCommand("import", "Importar todos os dados no MongoDB"),
            BotCommand("addsudo", "Adicionar um usuário como sudoer"),
            BotCommand("delsudo", "Remover um usuário dos sudoers"),
            BotCommand("sudolist", "Listar todos os usuários sudo"),
            BotCommand("log", "Obter os registros do bot"),
            BotCommand("getvar", "Obter uma variável de ambiente específica"),
            BotCommand("delvar", "Excluir uma variável de ambiente específica"),
            BotCommand("setvar", "Definir uma variável de ambiente específica"),
            BotCommand("usage", "Obter informações sobre o uso do Dyno"),
            BotCommand("maintenance", "Ativar ou desativar o modo de manutenção"),
            BotCommand("logger", "Ativar ou desativar o registro de atividades"),
            BotCommand("block", "Bloquear um usuário"),
            BotCommand("unblock", "Desbloquear um usuário"),
            BotCommand("blacklist", "Adicionar um chat à lista negra"),
            BotCommand("whitelist", "Remover um chat da lista negra"),
            BotCommand("blacklisted", "Listar todos os chats na lista negra"),
            BotCommand(
                "autoend", "Ativar ou desativar o término automático para transmissões"
            ),
            BotCommand("reboot", "Reiniciar o bot"),
            BotCommand("restart", "Reiniciar o bot"),
        ]

        await self.set_bot_commands(
            private_commands, scope=BotCommandScopeAllPrivateChats()
        )
        await self.set_bot_commands(
            group_commands, scope=BotCommandScopeAllGroupChats()
        )
        await self.set_bot_commands(
            admin_commands, scope=BotCommandScopeAllChatAdministrators()
        )

        LOG_GROUP_ID = (
            f"@{config.LOG_GROUP_ID}"
            if isinstance(config.LOG_GROUP_ID, str)
            and not config.LOG_GROUP_ID.startswith("@")
            else config.LOG_GROUP_ID
        )

        for owner_id in config.OWNER_ID:
            try:
                await self.set_bot_commands(
                    owner_commands,
                    scope=BotCommandScopeChatMember(
                        chat_id=LOG_GROUP_ID, user_id=owner_id
                    ),
                )
                await self.set_bot_commands(
                    private_commands + owner_commands,
                    scope=BotCommandScopeChat(chat_id=owner_id),
                )
            except Exception as e:
                LOGGER(__name__).warning(
                    "Failed to set owner commands for user %s:", owner_id, exc_info=True
                )

        else:
            pass
        try:
            a = await self.get_chat_member(config.LOG_GROUP_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error("Please promote bot as admin in logger group")
                sys.exit()
        except Exception:
            pass
        get_me = await self.get_me()
        if get_me.last_name:
            self.name = get_me.first_name + " " + get_me.last_name
        else:
            self.name = get_me.first_name
        LOGGER(__name__).info(f"MusicBot started as {self.name}")

    async def stop(self):
        LOGGER(__name__).info("Bot is shutting down")
        await self.send_message(
            config.LOG_GROUP_ID,
            text=f"🛑 <u><b>{self.mention} Bot Desligado :</b></u>\n\n🆔 <b>ID</b>: <code>{self.id}</code>\n📛 <b>Nome</b>: {self.name}\n🔗 <b>Nome de usuário:</b> @{self.username}",
        )
        await super().stop()
