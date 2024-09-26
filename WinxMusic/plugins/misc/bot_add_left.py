from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import LOG, LOG_GROUP_ID
from WinxMusic import app
from WinxMusic.utils.database import delete_served_chat, get_assistant, is_on_off


@app.on_message(filters.new_chat_members)
async def join_watcher(_, message):
    try:
        if not await is_on_off(LOG):
            return
        userbot = await get_assistant(message.chat.id)
        chat = message.chat
        for members in message.new_chat_members:
            if members.id == app.id:
                count = await app.get_chat_members_count(chat.id)
                username = (
                    message.chat.username if message.chat.username else "chat privado"
                )
                msg = (
                    f"**Bot de música adicionado em um novo grupo #Novo_Grupo**\n\n"
                    f"**Nome do chat:** {message.chat.title}\n"
                    f"**ID do chat:** {message.chat.id}\n"
                    f"**Nome de usuário do chat:** @{username}\n"
                    f"**Número de membros do chat:** {count}\n"
                    f"**Adicionado por:** {message.from_user.mention}"
                )
                await app.send_message(
                    LOG_GROUP_ID,
                    text=msg,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "Adicionado por",
                                    url=f"tg://openmessage?user_id={message.from_user.id}",
                                )
                            ]
                        ]
                    ),
                )
                await userbot.join_chat(f"{username}")
    except Exception as e:
        print(f"Error: {e}")


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(_, message: Message):
    try:
        if not await is_on_off(LOG):
            return
        userbot = await get_assistant(message.chat.id)

        left_chat_member = message.left_chat_member
        if left_chat_member and left_chat_member.id == app.id:
            remove_by = (
                message.from_user.mention
                if message.from_user
                else "Usuário Desconhecido"
            )
            title = message.chat.title
            username = (
                f"@{message.chat.username}" if message.chat.username else "chat privado"
            )
            chat_id = message.chat.id
            left = (
                f"✫ <b><u>#Grupo_Saída</u></b> ✫\n"
                f"Nome do chat: {title}\n"
                f"ID do chat: {chat_id}\n\n"
                f"Removido por: {remove_by}"
            )
            await app.send_message(LOG_GROUP_ID, text=left)
            await delete_served_chat(chat_id)
            await userbot.leave_chat(chat_id)
    except Exception as e:
        print(f"Error: {e}")
