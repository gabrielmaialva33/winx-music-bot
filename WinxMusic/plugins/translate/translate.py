from gpytranslate import Translator
from pyrogram import filters

from WinxMusic import app
from config import BANNED_USERS
from strings import get_command

# ------------------------------------------------------------------------------- #

trans = Translator()

# Command
TRANSLATOR_COMMAND = get_command("TRANSLATOR_COMMAND")


# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(TRANSLATOR_COMMAND) & filters.group & ~BANNED_USERS)
async def translate(_, message) -> None:
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("**Responda a uma mensagem para traduzir!**")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = await trans.detect(to_translate)
            dest = args
    except IndexError:
        source = await trans.detect(to_translate)
        dest = "pt"
    translation = await trans(to_translate, sourcelang=source, targetlang=dest)
    reply = (
        f"**Traduzido de {source} para {dest}**:\n"
        f"`{translation.text}`"
    )
    await message.reply_text(reply)

# ------------------------------------------------------------------------------- #
