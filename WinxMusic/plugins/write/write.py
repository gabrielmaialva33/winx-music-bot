from pyrogram import filters
from pyrogram.types import Message

from WinxMusic import app
from config import BANNED_USERS
from strings import get_command

# ------------------------------------------------------------------------------- #

# Command
WRITE_COMMAND = get_command("WRITE_COMMAND")


# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(WRITE_COMMAND) & filters.group & ~BANNED_USERS)
async def handwrite(_, message: Message):
    if not message.reply_to_message:
        name = (
            message.text.split(None, 1)[1]
            if len(message.command) < 3
            else message.text.split(None, 1)[1].replace(" ", "%20")
        )
        m = await app.send_message(message.chat.id, "escrevendo..")
        photo = "https://apis.xditya.me/write?text=" + name
        await app.send_photo(message.chat.id, photo=photo)
        await m.delete()
    else:
        lol = message.reply_to_message.text
        name = lol.split(None, 0)[0].replace(" ", "%20")
        m = await app.send_message(message.chat.id, "escrevendo..")
        photo = "https://apis.xditya.me/write?text=" + name
        await app.send_photo(message.chat.id, photo=photo)
        await m.delete()
