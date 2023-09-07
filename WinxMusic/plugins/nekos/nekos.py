import aiohttp
import asyncio
from WinxMusic import app
from pyrogram import filters
from pyrogram.types import Message
import requests
from strings import get_command

# --------------------------------------------------------------------------------- #

NEKO_CUDDLE_COMMAND = get_command("NEKO_CUDDLE_COMMAND")
NEKO_SHRUG_COMMAND = get_command("NEKO_SHRUG_COMMAND")
NEKO_POKE_COMMAND = get_command("NEKO_POKE_COMMAND")
NEKO_FACEPALM_COMMAND = get_command("NEKO_FACEPALM_COMMAND")
NEKO_STARE_COMMAND = get_command("NEKO_STARE_COMMAND")
NEKO_POUT_COMMAND = get_command("NEKO_POUT_COMMAND")
NEKO_HANDHOLD_COMMAND = get_command("NEKO_HANDHOLD_COMMAND")
NEKO_WAVE_COMMAND = get_command("NEKO_WAVE_COMMAND")
NEKO_BLUSH_COMMAND = get_command("NEKO_BLUSH_COMMAND")
NEKO_NEKO_COMMAND = get_command("NEKO_NEKO_COMMAND")
NEKO_DANCE_COMMAND = get_command("NEKO_DANCE_COMMAND")
NEKO_BAKA_COMMAND = get_command("NEKO_BAKA_COMMAND")
NEKO_BORE_COMMAND = get_command("NEKO_BORE_COMMAND")
NEKO_LAUGH_COMMAND = get_command("NEKO_LAUGH_COMMAND")
NEKO_SMUG_COMMAND = get_command("NEKO_SMUG_COMMAND")
NEKO_THUMBSUP_COMMAND = get_command("NEKO_THUMBSUP_COMMAND")
NEKO_SHOOT_COMMAND = get_command("NEKO_SHOOT_COMMAND")
NEKO_TICKLE_COMMAND = get_command("NEKO_TICKLE_COMMAND")
NEKO_FEED_COMMAND = get_command("NEKO_FEED_COMMAND")
NEKO_THINK_COMMAND = get_command("NEKO_THINK_COMMAND")
NEKO_WINK_COMMAND = get_command("NEKO_WINK_COMMAND")
NEKO_SLEEP_COMMAND = get_command("NEKO_SLEEP_COMMAND")
NEKO_PUNCH_COMMAND = get_command("NEKO_PUNCH_COMMAND")
NEKO_CRY_COMMAND = get_command("NEKO_CRY_COMMAND")
NEKO_KILL_COMMAND = get_command("NEKO_KILL_COMMAND")
NEKO_SMILE_COMMAND = get_command("NEKO_SMILE_COMMAND")
NEKO_HIGHFIVE_COMMAND = get_command("NEKO_HIGHFIVE_COMMAND")
NEKO_SLAP_COMMAND = get_command("NEKO_SLAP_COMMAND")
NEKO_HUG_COMMAND = get_command("NEKO_HUG_COMMAND")
NEKO_PAT_COMMAND = get_command("NEKO_PAT_COMMAND")
NEKO_WAIFU_COMMAND = get_command("NEKO_WAIFU_COMMAND")


# --------------------------------------------------------------------------------- #


@app.on_message(filters.command(NEKO_CUDDLE_COMMAND))
def cuddle(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/cuddle").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/cuddle").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_SHRUG_COMMAND))
def shrug(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/shrug").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/shrug").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_POKE_COMMAND))
def poke(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/poke").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/poke").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_FACEPALM_COMMAND))
def facepalm(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/facepalm").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/facepalm").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_STARE_COMMAND))
def stare(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/stare").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/stare").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_POUT_COMMAND))
def pout(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/pout").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/pout").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_HANDHOLD_COMMAND))
def handhold(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/handhold").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/handhold").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_WAVE_COMMAND))
def wave(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/wave").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/wave").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_BLUSH_COMMAND))
def blush(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/blush").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/blush").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_NEKO_COMMAND))
def neko(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/neko").json()
        url = api["results"][0]['url']
        reply.reply_photo(url)
    else:
        api = requests.get("https://nekos.best/api/v2/neko").json()
        url = api["results"][0]['url']
        m.reply_photo(url)

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_DANCE_COMMAND))
def dance(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/dance").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/dance").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** vamu dançã mana** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_BAKA_COMMAND))
def baka(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/baka").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/baka").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_BORE_COMMAND))
def bore(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/bored").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/bored").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_LAUGH_COMMAND))
def laugh(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/laugh").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/laugh").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_SMUG_COMMAND))
def smug(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/smug").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"** gaba de ** {m.from_user.first_name} **para** {reply.from_user.first_name}  🌈")
    else:
        api = requests.get("https://nekos.best/api/v2/smug").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** gaba de ** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_THUMBSUP_COMMAND))
def thumbsup(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/thumbsup").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"** joinha de ** {m.from_user.first_name} **para** {reply.from_user.first_name}  🌈")
    else:
        api = requests.get("https://nekos.best/api/v2/thumbsup").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** joinha de ** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_SHOOT_COMMAND))
def shoot(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/shoot").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"** tiro de ** {m.from_user.first_name} **para** {reply.from_user.first_name}")
    else:
        api = requests.get("https://nekos.best/api/v2/shoot").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** tiro de ** {m.from_user.first_name}")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_TICKLE_COMMAND))
def tickle(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/tickle").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"** cócegas de ** {m.from_user.first_name} **para** {reply.from_user.first_name}  🌈")
    else:
        api = requests.get("https://nekos.best/api/v2/tickle").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** cócegas de ** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_FEED_COMMAND))
def feed(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/feed").json()
        url = api["results"][0]['url']
        reply.reply_animation(url)
    else:
        api = requests.get("https://nekos.best/api/v2/feed").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_THINK_COMMAND))
def think(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/think").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"** pensando sobre de ** {m.from_user.first_name} **para** {reply.from_user.first_name} ")
    else:
        api = requests.get("https://nekos.best/api/v2/think").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** pensamentos de ** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_WINK_COMMAND))
def wink(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/wink").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"** piscadinha de ** {m.from_user.first_name} **para** {reply.from_user.first_name}  🌈")
    else:
        api = requests.get("https://nekos.best/api/v2/wink").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"** piscadinha de ** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_SLEEP_COMMAND))
def sleep(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/sleep").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"**vamu durmi mana** {reply.from_user.first_name}  🌈")
    else:
        api = requests.get("https://nekos.best/api/v2/sleep").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"**vamu durmi mana** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_PUNCH_COMMAND))
def punch(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://nekos.best/api/v2/punch").json()
        url = api["results"][0]['url']
        reply.reply_animation(url, caption=f"{m.from_user.first_name} **soca** {reply.from_user.first_name}")
    else:
        api = requests.get("https://nekos.best/api/v2/punch").json()
        url = api["results"][0]['url']
        m.reply_animation(animation=url, caption=f"**soco de** {m.from_user.first_name} ಠ‿ಠ")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_CRY_COMMAND))
def cry(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/cry").json()
        url = api["url"]
        reply.reply_animation(url, caption=f"{m.from_user.first_name} **chora poe** {reply.from_user.first_name}")
    else:
        api = requests.get("https://api.waifu.pics/sfw/cry").json()
        url = api["url"]
        m.reply_animation(animation=url, caption=f"{m.from_user.first_name} **chora**")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_KILL_COMMAND))
def kill(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/kill").json()
        url = api["url"]
        reply.reply_animation(url, caption=f"{m.from_user.first_name} **mata** {reply.from_user.first_name}")
    else:
        api = requests.get("https://api.waifu.pics/sfw/kill").json()
        url = api["url"]
        m.reply_animation(animation=url, caption=f"{m.from_user.first_name} **mata**")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_SMILE_COMMAND))
def smile(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/smile").json()
        url = api["url"]
        reply.reply_animation(url)
    else:
        api = requests.get("https://api.waifu.pics/sfw/smile").json()
        url = api["url"]
        m.reply_animation(animation=url, caption=f"** sorriso de ** {reply.from_user.first_name}  🌈")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_HIGHFIVE_COMMAND))
def highfive(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/highfive").json()
        url = api["url"]
        reply.reply_animation(url)
    else:
        api = requests.get("https://api.waifu.pics/sfw/highfive").json()
        url = api["url"]
        m.reply_animation(animation=url)
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_SLAP_COMMAND))
def slap(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/slap").json()
        url = api["url"]
        name1 = reply.from_user.first_name
        name2 = m.from_user.first_name
        reply.reply_animation(url, caption="{} (((;ꏿ_ꏿ;))) tapas {} ಠಗಠ".format(name2, name1))
    else:
        api = requests.get("https://api.waifu.pics/sfw/slap").json()
        url = api["url"]
        m.reply_animation(url, caption=f"**tapas de** {m.from_user.first_name} ಠ‿ಠ")
    m.delete()

# --------------------------------------------------------------------------------- #


@app.on_message(filters.command(NEKO_HUG_COMMAND))
def hug(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/hug").json()
        url = api["url"]
        name1 = reply.from_user.first_name
        name2 = m.from_user.first_name
        reply.reply_animation(url, caption="{} ( ◜‿◝ )♡ abraces {} ( ╹▽╹ )".format(name2, name1))
    else:
        api = requests.get("https://api.waifu.pics/sfw/hug").json()
        url = api["url"]
        m.reply_animation(animation=url, caption=f"**abraços de** {m.from_user.first_name} ( ◜‿◝ )♡")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_PAT_COMMAND))
def pat(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/pat").json()
        url = api["url"]
        name1 = reply.from_user.first_name
        name2 = m.from_user.first_name
        reply.reply_animation(url, caption="{} ( ◜‿◝ )♡ amoes {} ( ╹▽╹ )".format(name2, name1))
    else:
        api = requests.get("https://api.waifu.pics/sfw/pat").json()
        url = api["url"]
       #m.reply_animation(animation=url, caption=f"**ᴘᴀᴛs ʏᴏᴜ ᴀʟʟ ʟᴏᴠᴇs** {m.from_user.first_name}")
        m.reply_animation(animation=url, caption=f"** amoes de ** {m.from_user.first_name}")
    m.delete()

# --------------------------------------------------------------------------------- #

@app.on_message(filters.command(NEKO_WAIFU_COMMAND))
def waifu(_, m: Message):
    reply = m.reply_to_message
    if reply:
        api = requests.get("https://api.waifu.pics/sfw/waifu").json()
        url = api["url"]
        reply.reply_photo(url)
    else:
        api = requests.get("https://api.waifu.pics/sfw/waifu").json()
        url = api["url"]
        m.reply_photo(photo=url)

# --------------------------------------------------------------------------------- #


PALM_API_URL = "https://api.qewertyy.me/models"
MODEL_ID = 0
API_TIMEOUT = 10


async def get_palm_response(session, api_params):
    async with session.post(PALM_API_URL, params=api_params) as response:
        if response.status == 200:
            data = await response.json()
            return data.get(
                "content", "Error: Resposta vazia recebida da API PALM."
            )
        else:
            return f"Error: Request failed with status code {response.status}."


@app.on_message(filters.regex(r"^winx$"))
async def palm_chatbot(_client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("amoe.. mana 🌈")
        return

    input_text = args[1]

    try:
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=API_TIMEOUT)
        ) as session:
            result_msg = await message.reply("...")

            api_params = {"model_id": MODEL_ID, "prompt": input_text}
            api_response = await asyncio.gather(get_palm_response(session, api_params))

            await result_msg.delete()

    except aiohttp.ClientError as e:
        api_response = f"Error: An error occurred while calling the hiroko api. {e}"
    except asyncio.TimeoutError:
        api_response = "Error: The hiroko api request timed out."

    reply = message.reply_to_message
    if reply:
        await reply.reply(api_response[0])
    else:
        await message.reply(api_response[0])

# --------------------------------------------------------------------------------- #
