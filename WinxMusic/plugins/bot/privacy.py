from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

import config
from WinxMusic import app

TEXT = f"""
🔒 **Política de Privacidade do {app.mention}!**

Sua privacidade é importante para nós. Para saber mais sobre como coletamos, usamos e protegemos seus dados, por favor, revise nossa Política de Privacidade aqui: [Política de Privacidade]({config.PRIVACY_LINK}).

Se você tiver quaisquer perguntas ou preocupações, sinta-se à vontade para entrar em contato com nossa [Equipe de Suporte]({config.SUPPORT_GROUP}).
"""


@app.on_message(filters.command("privacy"))
async def privacy(_client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Ver Política de Privacidade", url=config.PRIVACY_LINK)]]
    )
    await message.reply_text(
        TEXT,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )
