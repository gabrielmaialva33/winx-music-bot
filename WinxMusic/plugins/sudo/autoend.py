from pyrogram import Client, filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import autoend_off, autoend_on
from strings import get_command

AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(_client: Client, message: Message):
    usage = "**Uso:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "Auto End Stream Ativado.\n\nO bot sairá automaticamente do chat de voz após 30 segundos se ninguém estiver ouvindo, com uma mensagem de aviso."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("Auto End Stream Desativado")
    else:
        await message.reply_text(usage)
