from pyrogram import filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.core.call import Winx
from WinxMusic.utils.database import is_music_playing, music_on
from WinxMusic.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

RESUME_COMMAND = get_command("RESUME_COMMAND")


@app.on_message(filters.command(RESUME_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_rights_check
async def resume_com(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text(_["general_2"])
    if await is_music_playing(chat_id):
        return await message.reply_text(_["admin_3"])
    await music_on(chat_id)
    await Winx.resume_stream(chat_id)
    await message.reply_text(_["admin_4"].format(message.from_user.mention))
