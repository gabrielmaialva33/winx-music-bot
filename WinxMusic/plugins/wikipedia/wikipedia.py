import requests
from PIL import Image, ImageDraw
from io import BytesIO
from WinxMusic import app
from pyrogram import Client, filters
from strings import get_command
from config import BANNED_USERS

# ------------------------------------------------------------------------------- #

# Command
WIKIPEDIA_COMMAND = get_command("WIKIPEDIA_COMMAND")

# ------------------------------------------------------------------------------- #


@app.on_message(filters.command(WIKIPEDIA_COMMAND) & filters.group & ~BANNED_USERS)
def handle_search(client: Client, message):
    query = message.text.split(None, 1)[1]
    url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{query}"
    response = requests.get(url)
    data = response.json()

    if 'extract' in data:
        result = data['extract']
    else:
        result = "Desculpe, não encontrei nada."

    image = Image.new('RGB', (500, 500))
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), result, fill=(255, 255, 255))

    image_file = BytesIO()
    image.save(image_file, 'PNG')
    image_file.seek(0)

    client.send_photo(message.chat.id, photo=image_file,
                      caption=f"**Wikipedia: {query}** \n\n**Resultado:**\n{result}")


