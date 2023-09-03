import logging
from pyrogram import filters
import requests
from WinxMusic import app
from strings import get_command

WIFU_COMMAND = get_command("WIFU_COMMAND")

# Define your bot token
TOKEN = "409K8eK4Ae_d6URhndD4RPyLkZ0pFeOp387ZATl8exox71TdYJpCkHj3AiQljp50X6gkptKrKQUCp419unNxddZlgEeGzwPxbTwYP21OcmbLjNmIIFVteTALHIbaVJGBWwEp9FoQUBAxNq5KPMKMvMv0Hr1ctzJMHEAiZMWZvhE"

# Define the API endpoint to fetch waifu images
API_ENDPOINT_1 = "https://api.waifu.pics/sfw/waifu"
API_ENDPOINT_2 = "https://nekos.best/api/v2/waifu/"


headers = {
    'Accept-Version': 'v5',
    'Authorization': 'Bearer ' + TOKEN,
}


def waifu():
    try:
        response = requests.get(API_ENDPOINT_1, headers=headers)
        data = response.json()
        image_url = data["url"]
        return image_url
    except Exception as e:
        logging.error(str(e))


@app.on_message(filters.command(WIFU_COMMAND))
async def wifu(client, message):
    # Send a message
    # await message.reply_text("Here is your waifu!")
    # Get the image URL
    image_url = waifu()
    # Send the image URL
    await message.reply_photo(image_url)
