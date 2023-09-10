import requests
from pyrogram import filters

from WinxMusic import app
from config import BANNED_USERS
from strings import get_command

# ------------------------------------------------------------------------------- #

# Command
WIKIPEDIA_COMMAND = get_command("WIKIPEDIA_COMMAND")


# ------------------------------------------------------------------------------- #


@app.on_message(filters.command(WIKIPEDIA_COMMAND) & filters.group & ~BANNED_USERS)
def handle_search(_, message):
    query = message.text.split(None, 1)[1]
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    data = response.json()

    if 'extract' in data:
        result = data['extract']
    else:
        result = "Desculpe, não encontrei nada."

    message.reply_text(result)
