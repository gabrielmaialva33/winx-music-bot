from pyrogram import filters, Client
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.utils.database.memorydatabase import get_loop, set_loop
from WinxMusic.utils.decorators import admin_rights_check
from config import BANNED_USERS, PREFIXES
from strings import get_command

LOOP_COMMAND = get_command("LOOP_COMMAND")


@app.on_message(filters.command(LOOP_COMMAND, PREFIXES) & filters.group & ~BANNED_USERS)
@admin_rights_check
async def admins(_client: Client, message: Message, _, chat_id: int):
    usage = _["admin_24"]
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            got = await get_loop(chat_id)
            if got != 0:
                state = got + state
            if int(state) > 10:
                state = 10
            await set_loop(chat_id, state)
            return await message.reply_text(
                _["admin_25"].format(message.from_user.first_name, state)
            )
        else:
            return await message.reply_text(_["admin_26"])
    elif state.lower() == "enable":
        await set_loop(chat_id, 10)
        return await message.reply_text(
            _["admin_25"].format(message.from_user.first_name, 10)
        )
    elif state.lower() == "disable":
        await set_loop(chat_id, 0)
        return await message.reply_text(_["admin_27"])
    else:
        return await message.reply_text(usage)
