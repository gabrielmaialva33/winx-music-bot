from pyrogram import Client, filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.core.userbot import assistants
from WinxMusic.utils.assistant import get_assistant_details
from WinxMusic.utils.assistant import is_avl_assistant as assistant
from WinxMusic.utils.database import get_assistant, save_assistant, set_assistant
from WinxMusic.utils.decorators import AdminActual
from config import BANNED_USERS, LOG_GROUP_ID


@app.on_message(filters.command("changeassistant") & ~BANNED_USERS)
@AdminActual
async def assis_change(_client: Client, message: Message, _):
    if await assistant() == True:
        return await message.reply_text(
            "Desculpe senhor! No servidor do bot há apenas um assistente disponível, portanto, você não pode alterar o assistente"
        )
    usage = f"**Uso do comando incorreto detectado \n**Uso:**\n/changeassistant - para alterar o assistente do seu grupo atual para um assistente aleatório no servidor do bot"
    if len(message.command) > 2:
        return await message.reply_text(usage)
    a = await get_assistant(message.chat.id)
    DETAILS = f"O assistente do seu chat foi alterado de [{a.name}](https://t.me/{a.username}) "
    if not message.chat.id == LOG_GROUP_ID:
        try:
            await a.leave_chat(message.chat.id)
        except:
            pass
    b = await set_assistant(message.chat.id)
    DETAILS += f"para [{b.name}](https://t.me/{b.username})"
    try:
        await b.join_chat(message.chat.id)
    except:
        pass
    await message.reply_text(DETAILS, disable_web_page_preview=True)


@app.on_message(filters.command("setassistant") & ~BANNED_USERS)
@AdminActual
async def assis_set(client, message: Message, _):
    if await assistant():
        return await message.reply_text(
            "Desculpe senhor! No servidor do bot há apenas um assistente disponível, portanto, você não pode alterar o assistente"
        )
    usage = await get_assistant_details()
    if len(message.command) != 2:
        return await message.reply_text(usage, disable_web_page_preview=True)
    query = message.text.split(None, 1)[1].strip()
    if query not in assistants:
        return await message.reply_text(usage, disable_web_page_preview=True)
    a = await get_assistant(message.chat.id)
    try:
        await a.leave_chat(message.chat.id)
    except:
        pass
    await save_assistant(message.chat.id, query)
    b = await get_assistant(message.chat.id)
    try:
        await b.join_chat(message.chat.id)
    except:
        pass
    await message.reply_text(
        "**Detalhes do novo assistente do seu chat:**\nNome do Assistente: {b.name}\nNome de usuário: @{b.username}\nID: {b.id}",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command("checkassistant") & filters.group & ~BANNED_USERS)
@AdminActual
async def check_ass(client, message: Message, _):
    a = await get_assistant(message.chat.id)
    await message.reply_text(
        "**Detalhes do assistente do seu chat:**\nNome do Assistente: {a.name}\nNome de usuário: @{a.username}\nID do Assistente: {a.id}",
        disable_web_page_preview=True,
    )
