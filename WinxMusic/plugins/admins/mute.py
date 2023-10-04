from pyrogram import filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.core.call import Winx
from WinxMusic.utils.database import is_muted, mute_on
from WinxMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS
from strings import get_command

# Commands
MUTE_COMMAND = get_command("MUTE_COMMAND")


@app.on_message(
    filters.command(MUTE_COMMAND)
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def mute_admin(cli, message: Message, _, chat_id):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text(_["general_2"])
    if await is_muted(chat_id):
        return await message.reply_text(_["admin_5"])
    await mute_on(chat_id)
    await Winx.mute_stream(chat_id)
    await message.reply_text(
        _["admin_6"].format(message.from_user.mention)
    )
