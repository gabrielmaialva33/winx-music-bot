from pyrogram.enums import ChatType

from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import get_lang, is_commanddelete_on, is_maintenance
from strings import get_string


def language(mystic: callable):
    async def wrapper(_, message, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("pt")
        if not await is_maintenance():
            if message.from_user.id not in SUDOERS:
                if message.chat.type == ChatType.PRIVATE:
                    return await message.reply_text(language["maint_4"])
                return
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass
        return await mystic(_, message, language)

    return wrapper


def language_cb(mystic: callable):
    async def wrapper(_, CallbackQuery, **kwargs):
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            language = get_string(language)
        except:
            language = get_string("pt")
        if not await is_maintenance():
            if CallbackQuery.from_user.id not in SUDOERS:
                if CallbackQuery.message.chat.type == ChatType.PRIVATE:
                    return await CallbackQuery.answer(
                        language["maint_4"],
                        show_alert=True,
                    )
                return

        return await mystic(_, CallbackQuery, language)

    return wrapper


def language_start(mystic: callable):
    async def wrapper(_, message, **kwargs):
        try:
            language = await get_lang(message.chat.id)
            language = get_string(language)
        except:
            language = get_string("pt")
        return await mystic(_, message, language)

    return wrapper
