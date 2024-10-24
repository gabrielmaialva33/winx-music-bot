from pyrogram import filters

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import autoend_off, autoend_on
from strings import get_command

AUTOEND_COMMAND = get_command("AUTOEND_COMMAND")


@app.on_message(filters.command(AUTOEND_COMMAND) & SUDOERS)
async def auto_end_stream(client, message):
    usage = "**Uso:**\n\n/autoend [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await autoend_on()
        await message.reply_text(
            "🔚 Auto Encerramento ativado.\n\nO bot sairá automaticamente do chat de voz após 30 segundos se ninguém estiver ouvindo a música, com uma mensagem de aviso."
        )
    elif state == "disable":
        await autoend_off()
        await message.reply_text("🔕 Auto Encerramento desativado")
    else:
        await message.reply_text(usage)
