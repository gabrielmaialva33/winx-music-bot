#
# Copyright (C) 2021-2022 by Maia, < https://github.com/gabrielmaialva33 >.
#
# This file is part of < https://github.com/gabrielmaialva33/winx-music-bot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/gabrielmaialva33/winx-music-bot/blob/master/LICENSE >
#
# All rights reserved.


from pyrogram.types import Message

from WinxMusic import app

WORD = ["vc", "voce", "you", "v.c", "ce", "você", "🫵"]


@app.on_message()
async def reply_gab(client, message: Message):
    if message.from_user.id == 387011206:
        if any(word in message.text.lower() for word in WORD):
            await message.reply_text(
                "VC 🫵".format(message.from_user.mention)
            )
