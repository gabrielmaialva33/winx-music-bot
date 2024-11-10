import logging
from functools import wraps
from traceback import format_exc as err

from pyrogram import Client
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS


async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = (await app.get_chat_member(chat_id, user_id)).privileges
    if not member:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_video_chats:
        perms.append("can_manage_video_chats")
    return perms


async def authorised(
        func: callable,
        sub_func2: callable,
        client: Client,
        message: Message,
        *args: list,
        **kwargs: dict,
):
    chat_id = message.chat.id
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await app.leave_chat(chat_id)
    except Exception as e:
        logging.exception(e)
        try:
            await message.reply_text(str(e.__class__.__name__) + ": " + str(e))
        except AttributeError:
            await message.reply_text(str(e))
        e = err()
        print(str(e))
    return sub_func2


async def unauthorised(
        message: Message, permission: str, sub_func2: callable, bot_lacking_permission=False
):
    chat_id = message.chat.id
    if bot_lacking_permission:
        text = (
                "Eu não tenho a permissão necessária para realizar esta ação."
                + f"\n**Permissão:** __{permission}__"
        )
    else:
        text = (
                "Você não tem a permissão necessária para realizar esta ação."
                + f"\n**Permissão:** __{permission}__"
        )
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await app.leave_chat(chat_id)
    return sub_func2


async def bot_permissions(chat_id: int):
    perms = []
    bot_id = (await app.get_me()).id
    return await member_permissions(chat_id, bot_id)


def admins_only(permission: str):
    def sub_func(func: callable):
        @wraps(func)
        async def sub_func2(
                client: Client, message: Message, *args: list, **kwargs: dict
        ):
            chat_id = message.chat.id

            # check if the bot has the required permission
            bot_perms = await bot_permissions(chat_id)
            if permission not in bot_perms:
                return await unauthorised(
                    message, permission, sub_func2, bot_lacking_permission=True
                )

            if not message.from_user:
                # for anonymous admins
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func,
                        sub_func2,
                        client,
                        message,
                        *args,
                        **kwargs,
                    )
                return await unauthorised(message, permission, sub_func2)

            # For admins and sudo users
            user_id = message.from_user.id
            permissions = await member_permissions(chat_id, user_id)
            if user_id not in SUDOERS and permission not in permissions:
                return await unauthorised(message, permission, sub_func2)
            return await authorised(func, sub_func2, client, message, *args, **kwargs)

        return sub_func2

    return sub_func
