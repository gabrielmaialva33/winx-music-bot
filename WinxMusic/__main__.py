import asyncio
import importlib
import sys

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from WinxMusic import HELPABLE, LOGGER, app, userbot
from WinxMusic.core.call import Winx
from WinxMusic.plugins import ALL_MODULES
from WinxMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if sys.version_info < (3, 9):
        LOGGER("WinxMusic").error(
            "WinxMusic is optimized for Python 3.9 or higher. Exiting..."
        )
        sys.exit(1)

    if len(config.STRING_SESSIONS) == 0:
        LOGGER("WinxMusic").error(
            "No Assistant Clients Vars Defined!.. Exiting Process."
        )
        return
    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
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
    except Exception:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module(all_module)

        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("WinxMusic.plugins").info("Successfully Imported All Modules ")
    await userbot.start()
    await Winx.start()
    LOGGER("WinxMusic").info("Assistant Started Sucessfully")
    try:
        await Winx.stream_call(
            "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"
        )
    except NoActiveGroupCall:
        LOGGER("WinxMusic").error(
            "Please ensure the voice call in your log group is active."
        )
        sys.exit()

    await Winx.decorators()
    LOGGER("WinxMusic").info("WinxMusic Started Successfully")
    await idle()
    await app.stop()
    await userbot.stop()


if __name__ == "__main__":
    asyncio.get_event_loop_policy().get_event_loop().run_until_complete(init())
    LOGGER("WinxMusic").info("Stopping WinxMusic! GoodBye")
