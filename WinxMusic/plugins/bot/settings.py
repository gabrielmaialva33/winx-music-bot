from pyrogram import Client, filters
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from WinxMusic import app
from WinxMusic.utils.database import (
    add_nonadmin_chat,
    cleanmode_off,
    cleanmode_on,
    commanddelete_off,
    commanddelete_on,
    get_aud_bit_name,
    get_authuser,
    get_authuser_names,
    get_playmode,
    get_playtype,
    get_vid_bit_name,
    is_cleanmode_on,
    is_commanddelete_on,
    is_nonadmin_chat,
    remove_nonadmin_chat,
    save_audio_bitrate,
    save_video_bitrate,
    set_playmode,
    set_playtype,
)
from WinxMusic.utils.decorators.admins import ActualAdminCB
from WinxMusic.utils.decorators.language import language, languageCB
from WinxMusic.utils.inline.settings import (
    audio_quality_markup,
    auth_users_markup,
    cleanmode_settings_markup,
    playmode_users_markup,
    setting_markup,
    video_quality_markup,
)
from WinxMusic.utils.inline.start import private_panel
from config import BANNED_USERS, CLEANMODE_DELETE_MINS, OWNER_ID
from strings import get_command

SETTINGS_COMMAND = get_command("SETTINGS_COMMAND")


@app.on_message(filters.command(SETTINGS_COMMAND) & filters.group & ~BANNED_USERS)
@language
async def settings_mar(_client: Client, message: Message, _):
    buttons = setting_markup(_)
    await message.reply_text(
        _["setting_1"].format(message.chat.title, message.chat.id),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settings_helper") & ~BANNED_USERS)
@languageCB
async def settings_cb(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer(_["set_cb_8"])
    except:
        pass
    buttons = setting_markup(_)
    return await callback_query.edit_message_text(
        _["setting_1"].format(
            callback_query.message.chat.title,
            callback_query.message.chat.id,
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_markup(_client: Client, callback_query: CallbackQuery, _):
    try:
        await callback_query.answer()
    except Exception as e:
        print(f"An error occurred: {e}")

    if callback_query.message.chat.type == ChatType.PRIVATE:
        try:
            await app.resolve_peer(OWNER_ID[0])
            OWNER = OWNER_ID[0]
        except:
            OWNER = None
        buttons = private_panel(_, app.username, OWNER)
        try:
            await callback_query.edit_message_text(
                _["start_1"].format(app.mention),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except MessageNotModified:
            pass
    else:
        buttons = setting_markup(_)
        try:
            await callback_query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except MessageNotModified:
            pass


## Audio and Video Quality
async def gen_buttons_aud(_, aud: str):
    if aud == "STUDIO":
        buttons = audio_quality_markup(_, STUDIO=True)
    elif aud == "HIGH":
        buttons = audio_quality_markup(_, HIGH=True)
    elif aud == "MEDIUM":
        buttons = audio_quality_markup(_, MEDIUM=True)
    elif aud == "LOW":
        buttons = audio_quality_markup(_, LOW=True)
    return buttons


async def gen_buttons_vid(_, aud):
    if aud == "UHD_4K":
        buttons = video_quality_markup(_, UHD_4K=True)
    elif aud == "QHD_2K":
        buttons = video_quality_markup(_, QHD_2K=True)
    elif aud == "FHD_1080p":
        buttons = video_quality_markup(_, FHD_1080p=True)
    elif aud == "HD_720p":
        buttons = video_quality_markup(_, HD_720p=True)
    elif aud == "SD_480p":
        buttons = video_quality_markup(_, SD_480p=True)
    elif aud == "SD_360p":
        buttons = video_quality_markup(_, SD_360p=True)
    return buttons


# without admin rights


@app.on_callback_query(
    filters.regex(
        pattern=r"^(SEARCHANSWER|PLAYMODEANSWER|PLAYTYPEANSWER|AUTHANSWER|CMANSWER|COMMANDANSWER|CM|AQ|VQ|PM|AU)$"
    )
    & ~BANNED_USERS
)
@languageCB
async def without_admin_rights(_client: Client, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    if command == "SEARCHANSWER":
        try:
            return await callback_query.answer(_["setting_3"], show_alert=True)
        except:
            return
    if command == "PLAYMODEANSWER":
        try:
            return await callback_query.answer(_["setting_10"], show_alert=True)
        except:
            return
    if command == "PLAYTYPEANSWER":
        try:
            return await callback_query.answer(_["setting_11"], show_alert=True)
        except:
            return
    if command == "AUTHANSWER":
        try:
            return await callback_query.answer(_["setting_4"], show_alert=True)
        except:
            return
    if command == "CMANSWER":
        try:
            return await callback_query.answer(
                _["setting_9"].format(CLEANMODE_DELETE_MINS),
                show_alert=True,
            )
        except:
            return
    if command == "COMMANDANSWER":
        try:
            return await callback_query.answer(_["setting_14"], show_alert=True)
        except:
            return
    if command == "CM":
        try:
            await callback_query.answer(_["set_cb_5"], show_alert=True)
        except:
            pass
        sta = None
        cle = None
        if await is_cleanmode_on(callback_query.message.chat.id):
            cle = True
        if await is_commanddelete_on(callback_query.message.chat.id):
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)

    if command == "AQ":
        try:
            await callback_query.answer(_["set_cb_1"], show_alert=True)
        except:
            pass
        aud = await get_aud_bit_name(callback_query.message.chat.id)
        buttons = await gen_buttons_aud(_, aud)
    if command == "VQ":
        try:
            await callback_query.answer(_["set_cb_2"], show_alert=True)
        except:
            pass
        aud = await get_vid_bit_name(callback_query.message.chat.id)
        buttons = await gen_buttons_vid(_, aud)
    if command == "PM":
        try:
            await callback_query.answer(_["set_cb_4"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "AU":
        try:
            await callback_query.answer(_["set_cb_3"], show_alert=True)
        except:
            pass
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            buttons = auth_users_markup(_, True)
        else:
            buttons = auth_users_markup(_)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Audio Video Quality


@app.on_callback_query(
    filters.regex(
        pattern=r"^(LOW|MEDIUM|HIGH|STUDIO|SD_360p|SD_480p|HD_720p|FHD_1080p|QHD_2K|UHD_4K)$"
    )
    & ~BANNED_USERS
)
@ActualAdminCB
async def aud_vid_cb(_client: Client, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    try:
        await callback_query.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "LOW":
        await save_audio_bitrate(callback_query.message.chat.id, "LOW")
        buttons = audio_quality_markup(_, LOW=True)
    if command == "MEDIUM":
        await save_audio_bitrate(callback_query.message.chat.id, "MEDIUM")
        buttons = audio_quality_markup(_, MEDIUM=True)
    if command == "HIGH":
        await save_audio_bitrate(callback_query.message.chat.id, "HIGH")
        buttons = audio_quality_markup(_, HIGH=True)
    if command == "STUDIO":
        await save_audio_bitrate(callback_query.message.chat.id, "STUDIO")
        buttons = audio_quality_markup(_, STUDIO=True)
    if command == "SD_360p":
        await save_video_bitrate(callback_query.message.chat.id, "SD_360p")
        buttons = video_quality_markup(_, SD_360p=True)
    if command == "SD_480p":
        await save_video_bitrate(callback_query.message.chat.id, "SD_480p")
        buttons = video_quality_markup(_, SD_480p=True)
    if command == "HD_720p":
        await save_video_bitrate(callback_query.message.chat.id, "HD_720p")
        buttons = video_quality_markup(_, HD_720p=True)
    if command == "FHD_1080p":
        await save_video_bitrate(callback_query.message.chat.id, "FHD_1080p")
        buttons = video_quality_markup(_, FHD_1080p=True)
    if command == "QHD_2K":
        await save_video_bitrate(callback_query.message.chat.id, "QHD_2K")
        buttons = video_quality_markup(_, QHD_2K=True)
    if command == "UHD_4K":
        await save_video_bitrate(callback_query.message.chat.id, "UHD_4K")
        buttons = video_quality_markup(_, UHD_4K=True)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


@app.on_callback_query(
    filters.regex(pattern=r"^(CLEANMODE|COMMANDELMODE)$") & ~BANNED_USERS
)
@ActualAdminCB
async def cleanmode_mark(_client: Client, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    try:
        await callback_query.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "CLEANMODE":
        sta = None
        if await is_commanddelete_on(callback_query.message.chat.id):
            sta = True
        cle = None
        if await is_cleanmode_on(callback_query.message.chat.id):
            await cleanmode_off(callback_query.message.chat.id)
        else:
            await cleanmode_on(callback_query.message.chat.id)
            cle = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    if command == "COMMANDELMODE":
        cle = None
        sta = None
        if await is_cleanmode_on(callback_query.message.chat.id):
            cle = True
        if await is_commanddelete_on(callback_query.message.chat.id):
            await commanddelete_off(callback_query.message.chat.id)
        else:
            await commanddelete_on(callback_query.message.chat.id)
            sta = True
        buttons = cleanmode_settings_markup(_, status=cle, dels=sta)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Play Mode Settings
@app.on_callback_query(
    filters.regex(pattern=r"^(|MODECHANGE|CHANNELMODECHANGE|PLAYTYPECHANGE)$")
    & ~BANNED_USERS
)
@ActualAdminCB
async def playmode_ans(_client: Client, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    if command == "CHANNELMODECHANGE":
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(callback_query.message.chat.id)
            Group = None
        else:
            await remove_nonadmin_chat(callback_query.message.chat.id)
            Group = True
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            Playtype = None
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "MODECHANGE":
        try:
            await callback_query.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            await set_playmode(callback_query.message.chat.id, "Inline")
            Direct = None
        else:
            await set_playmode(callback_query.message.chat.id, "Direct")
            Direct = True
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            Playtype = False
        else:
            Playtype = True
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    if command == "PLAYTYPECHANGE":
        try:
            await callback_query.answer(_["set_cb_6"], show_alert=True)
        except:
            pass
        playty = await get_playtype(callback_query.message.chat.id)
        if playty == "Everyone":
            await set_playtype(callback_query.message.chat.id, "Admin")
            Playtype = False
        else:
            await set_playtype(callback_query.message.chat.id, "Everyone")
            Playtype = True
        playmode = await get_playmode(callback_query.message.chat.id)
        if playmode == "Direct":
            Direct = True
        else:
            Direct = None
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            Group = True
        else:
            Group = None
        buttons = playmode_users_markup(_, Direct, Group, Playtype)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


# Auth Users Settings
@app.on_callback_query(filters.regex(pattern=r"^(AUTH|AUTHLIST)$") & ~BANNED_USERS)
@ActualAdminCB
async def authusers_mar(client: Client, callback_query: CallbackQuery, _):
    command = callback_query.matches[0].group(1)
    if command == "AUTHLIST":
        _authusers = await get_authuser_names(callback_query.message.chat.id)
        if not _authusers:
            try:
                return await callback_query.answer(_["setting_5"], show_alert=True)
            except:
                return
        else:
            try:
                await callback_query.answer(_["set_cb_7"], show_alert=True)
            except:
                pass
            j = 0
            await callback_query.edit_message_text(_["auth_6"])
            msg = _["auth_7"]
            for note in _authusers:
                _note = await get_authuser(callback_query.message.chat.id, note)
                user_id = _note["auth_user_id"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await client.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"   {_['auth_8']} {admin_name}[`{admin_id}`]\n\n"
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=_["BACK_BUTTON"], callback_data=f"AU"
                        ),
                        InlineKeyboardButton(
                            text=_["CLOSE_BUTTON"],
                            callback_data=f"close",
                        ),
                    ]
                ]
            )
            try:
                return await callback_query.edit_message_text(msg, reply_markup=upl)
            except MessageNotModified:
                return
    try:
        await callback_query.answer(_["set_cb_6"], show_alert=True)
    except:
        pass
    if command == "AUTH":
        is_non_admin = await is_nonadmin_chat(callback_query.message.chat.id)
        if not is_non_admin:
            await add_nonadmin_chat(callback_query.message.chat.id)
            buttons = auth_users_markup(_)
        else:
            await remove_nonadmin_chat(callback_query.message.chat.id)
            buttons = auth_users_markup(_, True)
    try:
        return await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    except MessageNotModified:
        return


"""✅<u>Gʀᴏᴜᴘ Sᴇᴛᴛɪɴɢs:</u>
/settings - Gᴇᴛ ᴀ ᴄᴏᴍᴘʟᴇᴛᴇ ɢʀᴏᴜᴘ's sᴇᴛᴛɪɴɢs ᴡɪᴛʜ ɪɴʟɪɴᴇ ʙᴜᴛᴛᴏɴs

🔗 <u>Oᴘᴛɪᴏɴs ɪɴ Sᴇᴛᴛɪɴɢs:</u>

1 Yᴏᴜ ᴄᴀɴ sᴇᴛ Aᴜᴅɪᴏ Qᴜᴀʟɪᴛʏ
2 Yᴏᴜ ᴄᴀɴ sᴇᴛ Vɪᴅᴇᴏ Qᴜᴀʟɪᴛʏ
3 **Aᴜᴛʜ Usᴇʀs**:- Yᴏᴜ ᴄᴀɴ ᴄʜᴀɴɢᴇ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs ᴍᴏᴅᴇ ғʀᴏᴍ ʜᴇʀᴇ ᴛᴏ ᴇᴠᴇʀʏᴏɴᴇ ᴏʀ ᴀᴅᴍɪɴs ᴏɴʟʏ.
4 **Cʟᴇᴀɴ Mᴏᴅᴇ:**ʙᴏᴛ's ᴅᴇʟᴇᴛᴇs ᴛʜᴇ ʙᴏᴛ's ᴍᴇssᴀɢᴇs ᴀғᴛᴇʀ 𝟻 ᴍɪɴs ғʀᴏᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ ᴍᴀᴋᴇ sᴜʀᴇ ʏᴏᴜʀ ᴄʜᴀᴛ ʀᴇᴍᴀɪɴs ᴄʟᴇᴀɴ ᴀɴᴅ ɢᴏᴏᴅ.
5 **Cᴏᴍᴍᴀɴᴅ Cʟᴇᴀɴ** : Wʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ, Bᴏᴛ ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ɪᴛs ᴇxᴇᴄᴜᴛᴇᴅ ᴄᴏᴍᴍᴀɴᴅs lɪᴍᴍᴇᴅɪᴀᴛᴇʟʏ.
       <b><u>Pʟᴀʏ Sᴇᴛᴛɪɴɢs:</></b>
/playmode - Gᴇᴛ ᴀ ᴄᴏᴍᴘʟᴇᴛᴇ ᴘʟᴀʏ sᴇᴛᴛɪɴɢs ᴘᴀɴᴇʟ ᴡɪᴛʜ ʙᴜᴛᴛᴏɴs ᴡʜᴇʀᴇ ʏᴏᴜ ᴄᴀɴ sᴇᴛ ʏᴏᴜʀ ɢʀᴏᴜᴘ's ᴘʟᴀʏ sᴇᴛᴛɪɴɢs. 
      <b><u>Oᴘᴛɪᴏɴs ɪɴ Pʟᴀʏᴍᴏᴅᴇ:</u></b>
1 **Sᴇᴀʀᴄʜ Mᴏᴅᴇ** [Dɪʀᴇᴄᴛ ᴏʀ Iɴʟɪɴᴇ] - Cʜᴀɴɢᴇs ʏᴏᴜʀ sᴇᴀʀᴄʜ ᴍᴏᴅᴇ ᴡʜɪʟᴇ ʏᴏᴜ ɢɪᴠᴇ /playmode
2 **Aᴅᴍɪɴ Cᴏᴍᴍᴀɴᴅs** [Eᴠᴇʀʏᴏɴᴇ ᴏʀ Aᴅᴍɪɴs] - Iғ ᴇᴠᴇʀʏᴏɴᴇ, ᴀɴʏᴏɴᴇ  ɪɴ ʏᴏᴜ ɢʀᴏᴜᴘ ᴡɪʟʟ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴜsᴇ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅ (ʟɪᴋᴇ /skip, /stop etc)
3 **Pʟᴀʏ Tʏᴘᴇ** [Eᴠᴇʀʏᴏɴᴇ ᴏʀ Aᴅᴍɪɴs] - Iғ ᴀᴅᴍɪɴs, ᴏɴʟʏ ɢʀᴏᴜᴘ ᴀᴅᴍɪɴs ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ.
"""
