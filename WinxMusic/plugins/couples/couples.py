import random
from datetime import datetime

from pyrogram import filters

from WinxMusic import app
from WinxMusic.utils.database.couplesdb import get_couple, save_couple
from strings import get_command


# Date and time
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
            str(int(dt()[0].split("/")[0]) + 1)
            + "/"
            + dt()[0].split("/")[1]
            + "/"
            + dt()[0].split("/")[2]
    )
    return a


today = str(dt()[0])
tomorrow = str(dt_tom())

# --------------------------------------------------------------------------------- #

COUPLE_COMMAND = get_command("COUPLE_COMMAND")


# --------------------------------------------------------------------------------- #


@app.on_message(filters.command(COUPLE_COMMAND) & filters.group)
async def couple(_, message):
    chat_id = message.chat.id
    is_selected = await get_couple(chat_id, date=today)

    if not is_selected:
        list_of_users = []
        async for i in app.get_chat_members(message.chat.id, limit=100):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)
        if len(list_of_users) < 2:
            return await message.reply_text("Não há membros suficientes para escolher um casal")
        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)
        c1_mention = (await app.get_users(c1_id)).mention
        c2_mention = (await app.get_users(c2_id)).mention

        couple_selection_message = f"""**⚜ 🌈 Casal do dia 🎡**

{c1_mention} + {c2_mention} = ❤️‍🔥
Novos casais serão escolhidos amanhã às 12h {tomorrow}"""
        await app.send_photo(message.chat.id, photo="https://telegra.ph/file/908be770f3a34834379f1.png",
                             caption=couple_selection_message)
        couple = {"c1_id": c1_id, "c2_id": c2_id}
        await save_couple(chat_id, today, couple)

    elif is_selected:
        c1_id = int(is_selected["c1_id"])
        c2_id = int(is_selected["c2_id"])
        c1_name = (await app.get_users(c1_id)).mention
        c2_name = (await app.get_users(c2_id)).mention
        couple_selection_message = f"""⚜ **Casal do dia :**

{c1_name} + {c2_name} = ❤️‍🔥
Novo casais serão escolhidos amanhã às 12h {tomorrow}"""
        await app.send_photo(message.chat.id, photo="https://telegra.ph/file/908be770f3a34834379f1.png",
                             caption=couple_selection_message)
