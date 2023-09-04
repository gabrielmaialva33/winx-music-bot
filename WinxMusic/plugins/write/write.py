from traceback import format_exc

from aiohttp import ClientSession
import requests
from PIL import Image, ImageDraw
from io import BytesIO
from Python_ARQ import ARQ
from WinxMusic import app
from pyrogram.types import Message
from pyrogram import Client, filters
from strings import get_command
from config import BANNED_USERS

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
