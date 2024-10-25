from pyrogram.types import CallbackQuery

from WinxMusic import app
from WinxMusic.utils.database import get_cmode


async def get_channeplay_cb(_, command: str, callback_query: CallbackQuery):
    if command == "c":
        chat_id = await get_cmode(callback_query.message.chat.id)
        if chat_id is None:
            try:
                return await callback_query.answer(_["setting_12"], show_alert=True)
            except:
                return
        try:
            chat = await app.get_chat(chat_id)
            channel = chat.title
        except:
            try:
                return await callback_query.answer(_["cplay_4"], show_alert=True)
            except:
                return
    else:
        chat_id = callback_query.message.chat.id
        channel = None
    return chat_id, channel
