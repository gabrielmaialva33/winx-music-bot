import logging
from pyrogram import filters
import requests
from WinxMusic import app
from strings import get_command

WIFU_COMMAND = get_command("WIFU_COMMAND")

# Define the API endpoint to fetch waifu images
API_ENDPOINT_1 = "https://api.waifu.pics/sfw/waifu"

def waifu():
    try:
        response = requests.get(API_ENDPOINT_1)
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
