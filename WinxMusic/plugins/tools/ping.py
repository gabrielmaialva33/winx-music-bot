from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.core.call import Winx
from WinxMusic.utils import bot_sys_stats
from WinxMusic.utils.decorators.language import language
from config import BANNED_USERS, MUSIC_BOT_NAME, PING_IMG_URL
from strings import get_command

### Commands
PING_COMMAND = get_command("PING_COMMAND")


@app.on_message(
    filters.command(PING_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@language
async def ping_com(_client, message: Message, _):
    response = await message.reply_animation(
        animation=PING_IMG_URL,
        caption=_["ping_1"],
    )
    start = datetime.now()
    pytgping = await Winx.ping()
    UP, CPU, RAM, DISK = await bot_sys_stats()
    resp = (datetime.now() - start).microseconds / 1000
    await response.edit_text(
        _["ping_2"].format(
            MUSIC_BOT_NAME, resp, UP, DISK, CPU, RAM, pytgping
        )
    )
