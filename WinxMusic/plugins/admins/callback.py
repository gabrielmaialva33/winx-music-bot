import random

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from WinxMusic import YouTube, app
from WinxMusic.core.call import Winx
from WinxMusic.misc import SUDOERS, db
from WinxMusic.utils.database import (
    is_active_chat,
    is_music_playing,
    is_muted,
    is_nonadmin_chat,
    music_off,
    music_on,
    mute_off,
    mute_on,
    set_loop,
)
from WinxMusic.utils.decorators.language import languageCB
from WinxMusic.utils.formatters import seconds_to_min
from WinxMusic.utils.inline.play import stream_markup, telegram_markup
from WinxMusic.utils.stream.autoclear import auto_clean
from WinxMusic.utils.thumbnails import gen_thumb
from config import (
    BANNED_USERS,
    SOUNCLOUD_IMG_URL,
    STREAM_IMG_URL,
    SUPPORT_GROUP,
    TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL,
    adminlist,
)

wrong = {}
down_vote = {}
down_voters = {}


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(_client: Client, callback_query: CallbackQuery, _):
    callback_data = callback_query.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await callback_query.answer(_["general_6"], show_alert=True)
    mention = callback_query.from_user.mention
    is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
    if not is_non_admin:
        if callback_query.from_user.id not in SUDOERS:
            admins = adminlist.get(callback_query.message.chat.id)
            if not admins:
                return await callback_query.answer(_["admin_18"], show_alert=True)
            else:
                if callback_query.from_user.id not in admins:
                    return await callback_query.answer(_["admin_19"], show_alert=True)
    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await callback_query.answer(_["admin_1"], show_alert=True)
        await callback_query.answer()
        await music_off(chat_id)
        await Winx.pause_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_2"].format(mention), disable_web_page_preview=True
        )
    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await callback_query.answer(_["admin_3"], show_alert=True)
        await callback_query.answer()
        await music_on(chat_id)
        await Winx.resume_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_4"].format(mention), disable_web_page_preview=True
        )
    elif command == "Stop" or command == "End":
        await callback_query.answer()
        await Winx.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await callback_query.message.reply_text(
            _["admin_9"].format(mention), disable_web_page_preview=True
        )
    elif command == "Mute":
        if await is_muted(chat_id):
            return await callback_query.answer(_["admin_5"], show_alert=True)
        await callback_query.answer()
        await mute_on(chat_id)
        await Winx.mute_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_6"].format(mention), disable_web_page_preview=True
        )
    elif command == "Unmute":
        if not await is_muted(chat_id):
            return await callback_query.answer(_["admin_7"], show_alert=True)
        await callback_query.answer()
        await mute_off(chat_id)
        await Winx.unmute_stream(chat_id)
        await callback_query.message.reply_text(
            _["admin_8"].format(mention), disable_web_page_preview=True
        )
    elif command == "Loop":
        await callback_query.answer()
        await set_loop(chat_id, 3)
        await callback_query.message.reply_text(_["admin_25"].format(mention, 3))

    elif command == "Shuffle":
        check = db.get(chat_id)
        if not check:
            return await callback_query.answer(_["admin_21"], show_alert=True)
        try:
            popped = check.pop(0)
        except:
            return await callback_query.answer(_["admin_22"], show_alert=True)
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await callback_query.answer(_["admin_22"], show_alert=True)
        await callback_query.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await callback_query.message.reply_text(
            _["admin_23"].format(mention), disable_web_page_preview=True
        )

    elif command == "Skip":
        check = db.get(chat_id)
        txt = f"» Faixa pulada por {mention}!"
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                await auto_clean(popped)
            if not check:
                await callback_query.edit_message_text(f"» Faixa pulada por {mention}!")
                await callback_query.message.reply_text(
                    _["admin_10"].format(mention), disable_web_page_preview=True
                )
                try:
                    return await Winx.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await callback_query.edit_message_text(f"» Faixa pulada por {mention}!")
                await callback_query.message.reply_text(
                    _["admin_10"].format(mention), disable_web_page_preview=True
                )
                return await Winx.stop_stream(chat_id)
            except:
                return
        await callback_query.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        duration_min = check[0]["dur"]
        callback_query.message.from_user.id
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await callback_query.message.reply_text(
                    _["admin_11"].format(title)
                )
            try:
                await Winx.skip_stream(chat_id, link, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            img = await gen_thumb(videoid)
            run = await callback_query.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    user,
                    f"https://t.me/{app.username}?start=info_{videoid}",
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await callback_query.edit_message_text(txt)
        elif "vid_" in queued:
            mystic = await callback_query.message.reply_text(
                _["call_8"], disable_web_page_preview=True
            )
            try:
                file_path, direct = await YouTube.download(
                    videoid,
                    mystic,
                    videoid=True,
                    video=status,
                )
            except:
                return await mystic.edit_text(_["call_7"])
            try:
                await Winx.skip_stream(chat_id, file_path, video=status)
            except Exception:
                return await mystic.edit_text(_["call_7"])
            button = stream_markup(_, videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await callback_query.message.reply_photo(
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await callback_query.edit_message_text(txt)
            await mystic.delete()
        elif "index_" in queued:
            try:
                await Winx.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            button = telegram_markup(_, chat_id)
            run = await callback_query.message.reply_photo(
                photo=STREAM_IMG_URL,
                caption=_["stream_2"].format(user),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await callback_query.edit_message_text(txt)
        else:
            try:
                await Winx.skip_stream(chat_id, queued, video=status)
            except Exception:
                return await callback_query.message.reply_text(_["call_7"])
            if videoid == "telegram":
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=(
                        TELEGRAM_AUDIO_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif videoid == "soundcloud":
                button = telegram_markup(_, chat_id)
                run = await callback_query.message.reply_photo(
                    photo=(
                        SOUNCLOUD_IMG_URL
                        if str(streamtype) == "audio"
                        else TELEGRAM_VIDEO_URL
                    ),
                    caption=_["stream_1"].format(
                        title, SUPPORT_GROUP, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                button = stream_markup(_, videoid, chat_id)
                img = await gen_thumb(videoid)
                run = await callback_query.message.reply_photo(
                    photo=img,
                    caption=_["stream_1"].format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        duration_min,
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            await callback_query.edit_message_text(txt)
    else:
        playing = db.get(chat_id)
        if not playing:
            return await callback_query.answer(_["queue_2"], show_alert=True)
        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await callback_query.answer(_["admin_30"], show_alert=True)
        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await callback_query.answer(_["admin_30"], show_alert=True)
        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]
        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await callback_query.answer(
                    f"» O bot não pode buscar porque a duração excede.\n\nAtualmente tocado: {bet} minutos de {duration} minutos.",
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await callback_query.answer(
                    f"» O bot não pode buscar porque a duração excede.\n\nAtualmente tocado: {bet} minutos de {duration} minutos.",
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1
        await callback_query.answer()
        mystic = await callback_query.message.reply_text(_["admin_32"])
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(_["admin_30"])
        try:
            await Winx.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
                playing[0]["streamtype"],
            )
        except:
            return await mystic.edit_text(_["admin_34"])
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = _["admin_33"].format(seconds_to_min(to_seek))
        await mystic.edit_text(f"{string}\n\nAlterações feitas por: {mention}!")


__MODULE__ = "Admin"
__HELP__ = """

<b>c significa reprodução de canal.</b>

<b>✧ /pause</b> ou <b>/cpause</b> - Pausa a música em reprodução.
<b>✧ /resume</b> ou <b>/cresume</b> - Retoma a música pausada.
<b>✧ /mute</b> ou <b>/cmute</b> - Silencia a música em reprodução.
<b>✧ /unmute</b> ou <b>/cunmute</b> - Ativa o som da música silenciada.
<b>✧ /skip</b> ou <b>/cskip</b> - Pula a música atual.
<b>✧ /stop</b> ou <b>/cstop</b> - Para a música em reprodução.
<b>✧ /shuffle</b> ou <b>/cshuffle</b> - Embaralha aleatoriamente a lista de reprodução em fila.
<b>✧ /seek</b> ou <b>/cseek</b> - Avança a música para a duração desejada.
<b>✧ /seekback</b> ou <b>/cseekback</b> - Retrocede a música para a duração desejada.
<b>✧ /reboot</b> - Reinicia o bot para o seu chat.

<b>✧ /skip</b> ou <b>/cskip</b> [Número (exemplo: 3)] - Pula para a música especificada na fila. Exemplo: <b>/skip 3</b> irá pular para a terceira música na fila, ignorando as músicas 1 e 2.

<b>✧ /loop</b> ou <b>/cloop</b> [ativar/desativar] ou [Números entre 1-10] - Quando ativado, o bot repete a música atual entre 1 e 10 vezes no chat de voz. Padrão para 10 vezes.
"""
