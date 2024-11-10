from pyrogram import filters, Client
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.core.call import Winx
from WinxMusic.utils.database import is_muted, mute_off, mute_on
from WinxMusic.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

MUTE_COMMAND = get_command("MUTE_COMMAND")
UNMUTE_COMMAND = get_command("UNMUTE_COMMAND")


@app.on_message(filters.command(MUTE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_rights_check
async def mute_admin(_client: Client, message: Message, _, chat_id: int):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text(_["general_2"])
    if await is_muted(chat_id):
        return await message.reply_text(_["admin_5"], disable_web_page_preview=True)
    await mute_on(chat_id)
    await Winx.mute_stream(chat_id)
    await message.reply_text(
        _["admin_6"].format(message.from_user.mention), disable_web_page_preview=True
    )


@app.on_message(filters.command(UNMUTE_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_rights_check
async def unmute_admin(_client: Client, message: Message, _, chat_id: int):
    if not len(message.command) == 1 or message.reply_to_message:
        return await message.reply_text(_["general_2"])
    if not await is_muted(chat_id):
        return await message.reply_text(_["admin_7"], disable_web_page_preview=True)
    await mute_off(chat_id)
    await Winx.unmute_stream(chat_id)
    await message.reply_text(
        _["admin_8"].format(message.from_user.mention), disable_web_page_preview=True
    )
