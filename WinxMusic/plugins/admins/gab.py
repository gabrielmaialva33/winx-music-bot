#
# Copyright (C) 2021-2022 by Maia, < https://github.com/gabrielmaialva33 >.
#
# This file is part of < https://github.com/gabrielmaialva33/winx-music-bot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/gabrielmaialva33/winx-music-bot/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.utils.decorators import AdminRightsCheck
from config import BANNED_USERS


@app.on_message()
async def reply_gab(client, message: Message):
    if message.from_user.id == 387011206:
        await message.reply_text(
            "VC 🫵".format(message.from_user.mention)
        )
