import asyncio
import platform
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover, Client
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import CallbackQuery, InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from WinxMusic import app, Platform
from WinxMusic.core.userbot import assistants
from WinxMusic.misc import SUDOERS, pymongodb
from WinxMusic.plugins import ALL_MODULES
from WinxMusic.utils.database import (
    get_global_tops,
    get_particulars,
    get_queries,
    get_served_chats,
    get_served_users,
    get_sudoers,
    get_top_chats,
    get_topp_users,
)
from WinxMusic.utils.decorators.language import language, language_cb
from WinxMusic.utils.inline.stats import (
    back_stats_buttons,
    back_stats_markup,
    get_stats_markup,
    overallback_stats_markup,
    stats_buttons,
    top_ten_stats_markup,
)
from config import BANNED_USERS, PREFIXES
from strings import get_command

loop = asyncio.get_running_loop()

GSTATS_COMMAND = get_command("GSTATS_COMMAND")
STATS_COMMAND = get_command("STATS_COMMAND")


@app.on_message(filters.command(STATS_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def stats_global(_client: Client, message: Message, _):
    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)
    await message.reply_photo(
        photo=config.STATS_IMG_URL,
        caption=_["gstats_11"].format(app.mention) + " 📊",
        reply_markup=upl,
    )


@app.on_message(filters.command(GSTATS_COMMAND, PREFIXES) & ~BANNED_USERS)
@language
async def gstats_global(_client: Client, message: Message, _):
    mystic = await message.reply_text(_["gstats_1"] + " ⏳")
    stats = await get_global_tops()
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"] + " 🚫")

    def get_stats():
        results = {}
        for i in stats:
            top_list = stats[i]["spot"]
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit(_["gstats_2"] + " 🚫")
        videoid = None
        co = None
        for vidid, count in list_arranged.items():
            if vidid == "telegram":
                continue
            else:
                videoid = vidid
                co = count
            break
        return videoid, co

    try:
        videoid, co = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    (
        title,
        duration_min,
        duration_sec,
        thumbnail,
        vidid,
    ) = await Platform.youtube.details(videoid, True)
    title = title.title()
    final = f"🎶 **Faixas mais tocadas no {app.mention}** 🎶\n\n**Título:** {title}\n\nTocada **{co}** vezes"
    upl = get_stats_markup(_, True if message.from_user.id in SUDOERS else False)
    await app.send_photo(
        message.chat.id,
        photo=thumbnail,
        caption=final,
        reply_markup=upl,
    )
    await mystic.delete()


@app.on_callback_query(filters.regex("GetStatsNow") & ~BANNED_USERS)
@language_cb
async def top_users_ten(_client: Client, callback_query: CallbackQuery, _):
    chat_id = callback_query.message.chat.id
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    upl = back_stats_markup(_)
    try:
        await callback_query.answer()
    except:
        pass
    mystic = await callback_query.edit_message_text(
        _["gstats_3"].format(
            f"do {callback_query.message.chat.title}" if what == "Here" else what
        )
        + " 🔝"
    )
    if what == "Tracks":
        stats = await get_global_tops()
    elif what == "Chats":
        stats = await get_top_chats()
    elif what == "Users":
        stats = await get_topp_users()
    elif what == "Here":
        stats = await get_particulars(chat_id)
    if not stats:
        await asyncio.sleep(1)
        return await mystic.edit(_["gstats_2"] + " 🚫", reply_markup=upl)
    queries = await get_queries()

    def get_stats():
        results = {}
        for i in stats:
            top_list = stats[i] if what in ["Chats", "Users"] else stats[i]["spot"]
            results[str(i)] = top_list
            list_arranged = dict(
                sorted(
                    results.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
        if not results:
            return mystic.edit(_["gstats_2"] + " 🚫", reply_markup=upl)
        msg = ""
        limit = 0
        total_count = 0
        if what in ["Tracks", "Here"]:
            for items, count in list_arranged.items():
                total_count += count
                if limit == 10:
                    continue
                limit += 1
                details = stats.get(items)
                title = (details["title"][:35]).title()
                if items == "telegram":
                    msg += f"🔗[TelegramVídeos e mídias](https://t.me/telegram) **Tocado {count} vezes**\n\n"
                else:
                    msg += f"🔗 [{title}](https://www.youtube.com/watch?v={items}) **Tocado {count} vezes**\n\n"

            temp = (
                _["gstats_4"].format(
                    queries,
                    app.mention,
                    len(stats),
                    total_count,
                    limit,
                )
                if what == "Tracks"
                else _["gstats_7"].format(len(stats), total_count, limit)
            )
            msg = temp + msg
        return msg, list_arranged

    try:
        msg, list_arranged = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    limit = 0
    if what in ["Users", "Chats"]:
        for items, count in list_arranged.items():
            if limit == 10:
                break
            try:
                extract = (
                    (await app.get_users(items)).first_name
                    if what == "Users"
                    else (await app.get_chat(items)).title
                )
                if extract is None:
                    continue
                await asyncio.sleep(0.5)
            except:
                continue
            limit += 1
            msg += f"🔗`{extract}` Tocou {count} vezes no bot.\n\n"
        temp = (
            _["gstats_5"].format(limit, app.mention)
            if what == "Chats"
            else _["gstats_6"].format(limit, app.mention)
        )
        msg = temp + msg
    med = InputMediaPhoto(media=config.GLOBAL_IMG_URL, caption=msg + " 🎧")
    try:
        await callback_query.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await callback_query.message.reply_photo(
            photo=config.GLOBAL_IMG_URL, caption=msg + " 🎧", reply_markup=upl
        )


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@language_cb
async def overall_stats(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup(_)
    else:
        upl = back_stats_buttons(_)
    try:
        await callback_query.answer()
    except:
        pass
    await callback_query.edit_message_text(_["gstats_8"] + " 📈")
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    playlist_limit = config.SERVER_PLAYLIST_LIMIT
    fetch_playlist = config.PLAYLIST_FETCH_LIMIT
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "Sim"
    else:
        ass = "Não"
    text = f"""📊 **Estatísticas e informações do Bot:**

🧩 **Módulos importados:** {mod}
👥 **Chats atendidos:** {served_chats} 
👤 **Usuários atendidos:** {served_users} 
🚫 **Usuários bloqueados:** {blocked} 
🔑 **Usuários Sudo:** {sudoers} 

🔍 **Total de Consultas:** {total_queries} 
🤖 **Total de Assistentes:** {assistant}
💨 **Assistente de Saída Automática:** {ass}

⏳ **Duração de Reprodução:** {play_duration} minutos
🎵 **Download de Música:** {song} minutos
📀 **Playlist no Servidor do Bot:** {playlist_limit}
🎶 **Reprodução de Playlist:** {fetch_playlist}"""
    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await callback_query.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await callback_query.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )


@app.on_callback_query(filters.regex("bot_stats_sudo"))
@language_cb
async def overall_stats(_client: Client, callback_query: CallbackQuery, _):
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer(
            "🔐 Somente para usuários Sudo", show_alert=True
        )
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup(_)
    else:
        upl = back_stats_buttons(_)
    try:
        await callback_query.answer()
    except:
        pass
    await callback_query.edit_message_text(_["gstats_8"] + " 📊")
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}MHz"
    except:
        cpu_freq = "Não foi possível obter"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0 ** 3)
    total = str(total)
    used = hdd.used / (1024.0 ** 3)
    used = str(used)
    free = hdd.free / (1024.0 ** 3)
    free = str(free)
    mod = len(ALL_MODULES)
    db = pymongodb
    call = db.command("dbstats")
    datasize = call["dataSize"] / 1024
    datasize = str(datasize)
    storage = call["storageSize"] / 1024
    objects = call["objects"]
    collections = call["collections"]

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    text = f"""📊 **Estatísticas e informações do Bot:**

🧩 **Módulos importados:** {mod}
💻 **Plataforma:** {sc}
📊 **Memória RAM:** {ram}
🖥️ **Cores físicas:** {p_core}
🖥️ **Total de Cores:** {t_core}
⚙️ **Frequência do CPU:** {cpu_freq}

🐍 **Versão do Python:** {pyver.split()[0]}
📦 **Versão do Pyrogram:** {pyrover}
🎧 **Versão do Py-tgcalls:** {pytgver}
💾 **Armazenamento total:** {total[:4]} GiB
💽 **Armazenamento usado:** {used[:4]} GiB
📂 **Armazenamento livre:** {free[:4]} GiB

👥 **Chats atendidos:** {served_chats} 
👤 **Usuários atendidos:** {served_users} 
🚫 **Usuários bloqueados:** {blocked} 
🔑 **Usuários Sudo:** {sudoers} 

🗄️ **Armazenamento total do BD:** {storage} MB
🗃️ **Total de Coleções do BD:** {collections}
🔑 **Total de Chaves do BD:** {objects}
🔍 **Total de Consultas no Bot:** `{total_queries} `
    """
    med = InputMediaPhoto(media=config.STATS_IMG_URL, caption=text)
    try:
        await callback_query.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await callback_query.message.reply_photo(
            photo=config.STATS_IMG_URL, caption=text, reply_markup=upl
        )


@app.on_callback_query(
    filters.regex(pattern=r"^(TOPMARKUPGET|GETSTATS|GlobalStats)$") & ~BANNED_USERS
)
@language_cb
async def back_buttons(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except:
        pass
    command = callback_query.matches[0].group(1)
    if command == "TOPMARKUPGET":
        upl = top_ten_stats_markup(_)
        med = InputMediaPhoto(
            media=config.GLOBAL_IMG_URL,
            caption=_["gstats_9"] + " 🔝",
        )
        try:
            await callback_query.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await callback_query.message.reply_photo(
                photo=config.GLOBAL_IMG_URL,
                caption=_["gstats_9"] + " 🔝",
                reply_markup=upl,
            )
    if command == "GlobalStats":
        upl = get_stats_markup(
            _,
            True if callback_query.from_user.id in SUDOERS else False,
        )
        med = InputMediaPhoto(
            media=config.GLOBAL_IMG_URL,
            caption=_["gstats_10"].format(app.mention) + " 📊",
        )
        try:
            await callback_query.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await callback_query.message.reply_photo(
                photo=config.GLOBAL_IMG_URL,
                caption=_["gstats_10"].format(app.mention) + " 📊",
                reply_markup=upl,
            )
    if command == "GETSTATS":
        upl = stats_buttons(
            _,
            True if callback_query.from_user.id in SUDOERS else False,
        )
        med = InputMediaPhoto(
            media=config.STATS_IMG_URL,
            caption=_["gstats_11"].format(app.mention) + " 📊",
        )
        try:
            await callback_query.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await callback_query.message.reply_photo(
                photo=config.STATS_IMG_URL,
                caption=_["gstats_11"].format(app.mention) + " 📊",
                reply_markup=upl,
            )
