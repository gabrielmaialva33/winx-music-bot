import random
import string

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, Message

import config
from WinxMusic import (
    LOGGER,
    app, Platform,
)
from WinxMusic.utils import seconds_to_min, time_to_seconds
from WinxMusic.utils.database import is_video_allowed
from WinxMusic.utils.decorators.play import play_wrapper
from WinxMusic.utils.formatters import formats
from WinxMusic.utils.inline.play import (
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
)
from WinxMusic.utils.inline.playlist import botplaylist_markup
from WinxMusic.utils.logger import play_logs
from WinxMusic.utils.stream.stream import stream
from config import BANNED_USERS, lyrical
from strings import get_command

PLAY_COMMAND = get_command("PLAY_COMMAND")


@app.on_message(
    filters.command(
        PLAY_COMMAND,
        prefixes=["/", "!", "%", ",", "@", "#"],
    )
    & filters.group
    & ~BANNED_USERS
)
@play_wrapper
async def play_commnd(
        _client: Client,
        message: Message,
        _,
        chat_id: int,
        video: bool,
        channel: bool,
        playmode: str,
        url: str,
        fplay: bool,
):
    mystic = await message.reply_text(
        _["play_2"].format(channel) if channel else _["play_1"]
    )
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.mention
    audio_telegram = (
        (message.reply_to_message.audio or message.reply_to_message.voice)
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (message.reply_to_message.video or message.reply_to_message.document)
        if message.reply_to_message
        else None
    )
    if audio_telegram:
        if audio_telegram.file_size > config.TG_AUDIO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_5"])
        duration_min = seconds_to_min(audio_telegram.duration)
        if audio_telegram.duration > config.DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_6"].format(config.DURATION_LIMIT_MIN, duration_min)
            )
        file_path = await Platform.telegram.get_filepath(audio=audio_telegram)
        if await Platform.telegram.download(_, message, mystic, file_path):
            message_link = await Platform.telegram.get_link(message)
            file_name = await Platform.telegram.get_filename(audio_telegram, audio=True)
            dur = await Platform.telegram.get_duration(audio_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                if ex_type == "AssistantErr":
                    err = e
                else:
                    err = _["general_3"].format(ex_type)
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif video_telegram:
        if not await is_video_allowed(message.chat.id):
            return await mystic.edit_text(_["play_3"])
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(
                        _["play_8"].format(f"{' | '.join(formats)}")
                    )
            except:
                return await mystic.edit_text(
                    _["play_8"].format(f"{' | '.join(formats)}")
                )
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_9"])
        file_path = await Platform.telegram.get_filepath(video=video_telegram)
        if await Platform.telegram.download(_, message, mystic, file_path):
            message_link = await Platform.telegram.get_link(message)
            file_name = await Platform.telegram.get_filename(video_telegram)
            dur = await Platform.telegram.get_duration(video_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=True,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                if ex_type == "AssistantErr":
                    err = e
                else:
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                    err = _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif url:
        if await Platform.youtube.exists(url):
            if "playlist" in url:
                try:
                    details = await Platform.youtube.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                img = config.PLAYLIST_IMG_URL
                cap = _["play_10"]
            elif "https://youtu.be" in url:
                videoid = url.split("/")[-1].split("?")[0]
                details, track_id = await Platform.youtube.track(
                    f"https://www.youtube.com/watch?v={videoid}"
                )
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
            else:
                try:
                    details, track_id = await Platform.youtube.track(url)
                except Exception as e:
                    print(e)
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(
                    details["title"],
                    details["duration_min"],
                )
        elif await Platform.spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text(
                    "🚫 Este bot não pode reproduzir faixas e playlists do Spotify. Por favor, entre em contato com meu dono e peça para ele adicionar o reprodutor de Spotify."
                )
            if "track" in url:
                try:
                    details, track_id = await Platform.spotify.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Platform.spotify.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spplay"
                img = config.SPOTIFY_PLAYLIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "album" in url:
                try:
                    details, plist_id = await Platform.spotify.album(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spalbum"
                img = config.SPOTIFY_ALBUM_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            elif "artist" in url:
                try:
                    details, plist_id = await Platform.spotify.artist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "spartist"
                img = config.SPOTIFY_ARTIST_IMG_URL
                cap = _["play_12"].format(message.from_user.first_name)
            else:
                return await mystic.edit_text(_["play_17"])
        elif await Platform.apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Platform.apple.track(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Platform.apple.playlist(url)
                except Exception:
                    return await mystic.edit_text(_["play_3"])
                streamtype = "playlist"
                plist_type = "apple"
                cap = _["play_13"].format(message.from_user.first_name)
                img = url
            else:
                return await mystic.edit_text(_["play_16"])
        elif await Platform.resso.valid(url):
            try:
                details, track_id = await Platform.resso.track(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])
            streamtype = "youtube"
            img = details["thumb"]
            cap = _["play_11"].format(details["title"], details["duration_min"])
        elif await Platform.saavn.valid(url):
            if "shows" in url:
                return await mystic.edit_text(_["saavn_1"])

            elif await Platform.saavn.is_song(url):
                try:
                    file_path, details = await Platform.saavn.download(url)
                except Exception as e:
                    ex_type = type(e).__name__
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                    return await mystic.edit_text(_["play_3"])
                duration_sec = details["duration_sec"]
                streamtype = "saavn_track"

                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(
                        _["play_6"].format(
                            config.DURATION_LIMIT_MIN,
                            details["duration_min"],
                        )
                    )
            elif await Platform.saavn.is_playlist(url):
                try:
                    details = await Platform.saavn.playlist(
                        url, limit=config.PLAYLIST_FETCH_LIMIT
                    )
                    streamtype = "saavn_playlist"
                except Exception as e:
                    ex_type = type(e).__name__
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                    return await mystic.edit_text(_["play_3"])

                if len(details) == 0:
                    return await mystic.edit_text(_["play_3"])
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype=streamtype,
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                if ex_type == "AssistantErr":
                    err = e
                else:
                    err = _["general_3"].format(ex_type)
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                return await mystic.edit_text(err)
            return await mystic.delete()
        elif await Platform.soundcloud.valid(url):
            try:
                details, track_path = await Platform.soundcloud.download(url)
            except Exception:
                return await mystic.edit_text(_["play_3"])
            duration_sec = details["duration_sec"]
            if duration_sec > config.DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(
                        config.DURATION_LIMIT_MIN,
                        details["duration_min"],
                    )
                )
            try:
                await stream(
                    _,
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="soundcloud",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                if ex_type == "AssistantErr":
                    err = e
                else:
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                    err = _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await mystic.delete()
        else:
            if not await Platform.telegram.is_streamable_url(url):
                return await mystic.edit_text(_["play_19"])

            await mystic.edit_text(_["str_2"])
            try:
                await stream(
                    _,
                    mystic,
                    message.from_user.id,
                    url,
                    chat_id,
                    message.from_user.first_name,
                    message.chat.id,
                    video=video,
                    streamtype="index",
                    forceplay=fplay,
                )
            except Exception as e:
                ex_type = type(e).__name__
                if ex_type == "AssistantErr":
                    err = e
                else:
                    LOGGER(__name__).error("An error occurred", exc_info=True)
                    err = _["general_3"].format(ex_type)
                return await mystic.edit_text(err)
            return await play_logs(message, streamtype="M3u8 or Index Link")
    else:
        if len(message.command) < 2:
            buttons = botplaylist_markup(_)
            return await mystic.edit_text(
                _["playlist_1"],
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")
        try:
            details, track_id = await Platform.youtube.track(query)
        except Exception as e:
            print(e)
            return await mystic.edit_text(_["play_3"])
        streamtype = "youtube"
    if str(playmode) == "Direct" and not plist_type:
        if details["duration_min"]:
            duration_sec = time_to_seconds(details["duration_min"])
            if duration_sec > config.DURATION_LIMIT:
                return await mystic.edit_text(
                    _["play_6"].format(
                        config.DURATION_LIMIT_MIN,
                        details["duration_min"],
                    )
                )
        else:
            buttons = livestream_markup(
                _,
                track_id,
                user_id,
                "v" if video else "a",
                "c" if channel else "g",
                "f" if fplay else "d",
            )
            return await mystic.edit_text(
                _["play_15"],
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                streamtype=streamtype,
                spotify=spotify,
                forceplay=fplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            if ex_type == "AssistantErr":
                err = e
            else:
                LOGGER(__name__).error("An error occurred", exc_info=True)

                err = _["general_3"].format(ex_type)
            return await mystic.edit_text(err)
        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)
    else:
        if plist_type:
            ran_hash = "".join(
                random.choices(string.ascii_uppercase + string.digits, k=10)
            )
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(
                _,
                ran_hash,
                message.from_user.id,
                plist_type,
                "c" if channel else "g",
                "f" if fplay else "d",
            )
            await mystic.delete()
            await message.reply_photo(
                photo=img,
                caption=cap,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, streamtype=f"Playlist : {plist_type}")
        else:
            if slider:
                buttons = slider_markup(
                    _,
                    track_id,
                    message.from_user.id,
                    query,
                    0,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=details["thumb"],
                    caption=_["play_11"].format(
                        details["title"].title(),
                        details["duration_min"],
                    ),
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype=f"Searched on Youtube")
            else:
                buttons = track_markup(
                    _,
                    track_id,
                    message.from_user.id,
                    "c" if channel else "g",
                    "f" if fplay else "d",
                )
                await mystic.delete()
                await message.reply_photo(
                    photo=img,
                    caption=cap,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
                return await play_logs(message, streamtype=f"URL Searched Inline")


__MODULE__ = "Play"
__HELP__ = """
<b>★ play, vplay, cplay</b> - Comandos Disponíveis
<b>★ playforce, vplayforce, cplayforce</b> - Comandos de Reprodução Forçada

<b>✦ c significa reprodução em canal.</b>
<b>✦ v significa reprodução de vídeo.</b>
<b>✦ force significa reprodução forçada.</b>

<b>✧ /play ou /vplay ou /cplay</b> - O bot começará a reproduzir a consulta fornecida no chat de voz ou transmitirá links ao vivo nos chats de voz.

<b>✧ /playforce ou /vplayforce ou /cplayforce</b> - A Reprodução Forçada interrompe a faixa atual no chat de voz e começa a tocar a faixa pesquisada instantaneamente sem alterar/limpar a fila.

<b>✧ /channelplay [Nome de usuário ou ID do chat] ou [Desativar]</b> - Conecte um canal a um grupo e transmita música no chat de voz do canal a partir do seu grupo.

<b>✧ /stream [url] </b> - Transmita uma URL que você acredita ser direta ou m3u8 e que não pode ser reproduzida pelo comando /play.
"""
