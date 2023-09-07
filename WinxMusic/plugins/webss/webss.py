from base64 import b64decode
from inspect import getfullargspec
from io import BytesIO

from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import Message

from WinxMusic import app
from config import BANNED_USERS
from strings import get_command

# ------------------------------------------------------------------------------- #

aiohttpsession = ClientSession()

WEBSS_COMMAND = get_command("WEBSS_COMMAND")


# ------------------------------------------------------------------------------- #

async def post(url: str, *args, **kwargs):
    async with aiohttpsession.post(url, *args, **kwargs) as resp:
        try:
            data = await resp.json()
        except Exception:
            data = await resp.text()
    return data


async def take_screenshot(url: str, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    payload = {
        "url": url,
        "width": 1920,
        "height": 1080,
        "scale": 1,
        "format": "jpeg",
    }
    if full:
        payload["full"] = True
    data = await post(
        "https://webscreenshot.vercel.app/api",
        data=payload,
    )
    if "image" not in data:
        return None
    b = data["image"].replace("data:image/jpeg;base64,", "")
    file = BytesIO(b64decode(b))
    file.name = "webss.jpg"
    return file


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(WEBSS_COMMAND) & filters.group & ~BANNED_USERS)
async def take_ss(_, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="Me envie um link para tirar um print dele.")

    if len(message.command) == 2:
        url = message.text.split(None, 1)[1]
        full = False
    elif len(message.command) == 3:
        url = message.text.split(None, 2)[1]
        full = message.text.split(None, 2)[2].lower().strip() in [
            "yes",
            "y",
            "1",
            "true",
        ]
    else:
        return await eor(message, text="Comando inválido.")

    m = await eor(message, text="Tirando print...")

    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("Não consegui tirar print desse link.")

        m = await m.edit("Uploading...")

        if not full:
            await message.reply_photo(photo)
        else:
            await message.reply_photo(photo)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))
