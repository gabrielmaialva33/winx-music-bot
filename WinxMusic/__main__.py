import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from WinxMusic import LOGGER, app, userbot
from WinxMusic.core.call import Winx
from WinxMusic.plugins import ALL_MODULES
from WinxMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

loop = asyncio.get_event_loop_policy().get_event_loop()


async def init():
    if (
            not config.STRING1
            and not config.STRING2
            and not config.STRING3
            and not config.STRING4
            and not config.STRING5
            and not config.STRING6
    ):
        LOGGER("WinxMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if (
            not config.SPOTIFY_CLIENT_ID
            and not config.SPOTIFY_CLIENT_SECRET
    ):
        LOGGER("WinxMusic").warning(
            "No Spotify Vars defined. Your bot won't be able to play spotify queries."
        )
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("WinxMusic.plugins" + all_module)
    LOGGER("WinxMusic.plugins").info(
        "Successfully Imported Modules "
    )
    await userbot.start()
    await Winx.start()
    try:
        await Winx.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("WinxMusic").error(
            "[ERROR] - \n\nPlease turn on your Logger Group's Voice Call. Make sure you never close/end voice call in your log group"
        )
        sys.exit()
    except:
        pass
    await Winx.decorators()
    LOGGER("WinxMusic").info("Winx Music Bot Started Successfully")
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("WinxMusic").info("Stopping Winx Music Bot! GoodBye")
