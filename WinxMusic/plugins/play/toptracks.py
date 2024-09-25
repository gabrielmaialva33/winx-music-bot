import asyncio
import logging

from httpx import Client
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup

from config import BANNED_USERS
from WinxMusic import app
from WinxMusic.utils.database import (
    get_assistant,
    get_global_tops,
    get_particulars,
    get_userss,
)
from WinxMusic.utils.decorators.language import languageCB
from WinxMusic.utils.inline.playlist import (
    botplaylist_markup,
    failed_top_markup,
    top_play_markup,
)
from WinxMusic.utils.stream.stream import stream

loop = asyncio.get_running_loop()


@app.on_callback_query(filters.regex("get_playmarkup") & ~BANNED_USERS)
@languageCB
async def get_play_markup(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except:
        pass
    buttons = botplaylist_markup(_)
    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("get_top_playlists") & ~BANNED_USERS)
@languageCB
async def get_topz_playlists(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except:
        pass
    buttons = top_play_markup(_)
    return await callback_query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(filters.regex("SERVERTOP") & ~BANNED_USERS)
@languageCB
async def server_to_play(client: Client, callback_query: CallbackQuery, _):
    userbot = await get_assistant(callback_query.message.chat.id)
    try:
        try:
            get = await app.get_chat_member(callback_query.message.chat.id, userbot.id)
        except ChatAdminRequired:
            return await callback_query.answer(
                f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ᴛᴏ {callback_query.message.chat.title}.",
                show_alert=True,
            )
        if get.status == ChatMemberStatus.BANNED:
            return await callback_query.answer(
                text=f"»ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ {callback_query.message.chat.title}",
                show_alert=True,
            )
    except UserNotParticipant:
        if callback_query.message.chat.username:
            invitelink = callback_query.message.chat.username
            try:
                await userbot.resolve_peer(invitelink)
            except Exception as ex:
                logging.exception(ex)
        else:
            try:
                invitelink = await client.export_chat_invite_link(
                    callback_query.message.chat.id
                )
            except ChatAdminRequired:
                return await callback_query.answer(
                    f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.",
                    show_alert=True,
                )
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(
                        callback_query.message.chat.id, userbot.id
                    )
                except Exception as e:
                    return await callback_query.message.reply_text(
                        f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}\nʀᴇᴀsᴏɴ :{e}"
                    )
            except Exception as ex:
                if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                    return await callback_query.answer(
                        f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.",
                        show_alert=True,
                    )
                else:
                    return await callback_query.message.reply_text(
                        f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.\n\n**ʀᴇᴀsᴏɴ :** `{ex}`"
                    )
        if invitelink.startswith("https://t.me/+"):
            invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
        try:
            await userbot.join_chat(invitelink)
            await asyncio.sleep(2)
        except UserAlreadyParticipant:
            pass
        except InviteRequestSent:
            try:
                await app.approve_chat_join_request(
                    callback_query.message.chat.id, userbot.id
                )
            except Exception as e:
                if "messages.HideChatJoinRequest" in str(e):
                    return await callback_query.answer(
                        f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.",
                        show_alert=True,
                    )
                else:
                    return await callback_query.message.reply_text(
                        f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.\n\nʀᴇᴀsᴏɴ :{e}"
                    )
        except Exception as ex:
            if "channels.JoinChannel" in str(ex) or "Username not found" in str(ex):
                return await callback_query.answer(
                    f"» ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ ғᴏʀ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.",
                    show_alert=True,
                )
            else:
                return await callback_query.message.reply_text(
                    f"ғᴀɪʟᴇᴅ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴛᴏ {callback_query.message.chat.title}.\n\nʀᴇᴀsᴏɴ : {ex}"
                )

        try:
            await userbot.resolve_peer(invitelink)
        except:
            pass

    chat_id = callback_query.message.chat.id
    user_name = callback_query.from_user.first_name
    try:
        await callback_query.answer()
    except:
        pass
    callback_data = callback_query.data.strip()
    what = callback_data.split(None, 1)[1]
    mystic = await callback_query.edit_message_text(
        _["tracks_1"].format(
            what,
            callback_query.from_user.first_name,
        )
    )
    upl = failed_top_markup(_)
    if what == "Global":
        stats = await get_global_tops()
    elif what == "Group":
        stats = await get_particulars(chat_id)
    elif what == "Personal":
        stats = await get_userss(callback_query.from_user.id)
    if not stats:
        return await mystic.edit(_["tracks_2"].format(what), reply_markup=upl)

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
            return mystic.edit(_["tracks_2"].format(what), reply_markup=upl)
        details = []
        limit = 0
        for vidid, count in list_arranged.items():
            if vidid == "telegram":
                continue
            if limit == 10:
                break
            limit += 1
            details.append(vidid)
        if not details:
            return mystic.edit(_["tracks_2"].format(what), reply_markup=upl)
        return details

    try:
        details = await loop.run_in_executor(None, get_stats)
    except Exception as e:
        print(e)
        return
    try:
        await stream(
            _,
            mystic,
            callback_query.from_user.id,
            details,
            chat_id,
            user_name,
            callback_query.message.chat.id,
            video=False,
            streamtype="playlist",
        )
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_3"].format(ex_type)
        return await mystic.edit_text(err)
    return await mystic.delete()
