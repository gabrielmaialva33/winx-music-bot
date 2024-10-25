from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.utils.database import get_authuser_names
from WinxMusic.utils.decorators import language
from WinxMusic.utils.formatters import alpha_to_int
from config import BANNED_USERS, adminlist
from strings import get_command

RELOAD_COMMAND = get_command("RELOAD_COMMAND")


@app.on_message(filters.command(RELOAD_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def reload_admin_cache(_client: Client, message: Message, _):
    try:
        chat_id = message.chat.id
        admins = app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        async for user in admins:
            if user.privileges.can_manage_video_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
        await message.reply_text(_["admin_20"])
    except:
        await message.reply_text(
            "⚠️ Falha ao recarregar o cache de administradores. Certifique-se de que o bot é administrador no seu chat."
        )
