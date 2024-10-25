from pyrogram import filters
from pyrogram.errors import ChannelInvalid
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS, db
from WinxMusic.utils.database.memorydatabase import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from strings import command, get_command

ACTIVEVC_COMMAND = get_command("ACTIVEVC_COMMAND")
ACTIVEVIDEO_COMMAND = get_command("ACTIVEVIDEO_COMMAND")
AC_COMMAND = get_command("AC_COMMAND")


# Function for removing the Active voice and video chat also clear the db dictionary for the chat
async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


@app.on_message(filters.command(ACTIVEVC_COMMAND) & SUDOERS)
async def activevc(_, message: Message):
    mystic = await message.reply_text(
        "🎙️ Buscando chats de voz ativos....\nPor favor, aguarde"
    )
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalid:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit_text("🔍 Nenhum chat ativo encontrado")
    else:
        await mystic.edit_text(
            f"**Chats de Vídeo Ativos:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(ACTIVEVIDEO_COMMAND) & SUDOERS)
async def activevi_(_, message: Message):
    mystic = await message.reply_text(
        "🎙️ Buscando chats de voz ativos....\nPor favor, aguarde"
    )
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await app.get_chat(x)).title
            if (await app.get_chat(x)).username:
                user = (await app.get_chat(x)).username
                text += f"<b>{j + 1}.</b>  [{title}](https://t.me/{user})[`{x}`]\n"
            else:
                text += f"<b>{j + 1}. {title}</b> [`{x}`]\n"
            j += 1
        except ChannelInvalid:
            await _clear_(x)
            continue
    if not text:
        await mystic.edit_text("🔍 Nenhum chat ativo encontrado")
    else:
        await mystic.edit_text(
            f"**Chats de Vídeo Ativos:-**\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(AC_COMMAND) & SUDOERS)
async def vc(client, message: Message):
    ac_audio = str(len(await get_active_chats()))
    await message.reply_text(f"<b>Chats Ativos</b>: {ac_audio}")


__MODULE__ = "Ativo"
__HELP__ = f"""
<b>✧ {command("AC_COMMAND")}</b> - Verificar os chats de voz ativos no bot.

<b>✧ {command("ACTIVEVC_COMMAND")}</b> - Verificar as chamadas de voz e vídeo ativas no bot.

<b>✧ {command("ACTIVEVIDEO_COMMAND")}</b> - Verificar as chamadas de vídeo ativas no bot.

<b>✧ {command("STATS_COMMAND")}</b> - Verificar as estatísticas do bot.
"""
