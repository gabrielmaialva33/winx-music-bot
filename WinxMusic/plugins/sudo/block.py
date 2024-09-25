from pyrogram import Client, filters
from pyrogram.types import Message

from config import BANNED_USERS
from strings import get_command
from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import add_gban_user, remove_gban_user
from WinxMusic.utils.decorators.language import language

BLOCK_COMMAND = get_command("BLOCK_COMMAND")
UNBLOCK_COMMAND = get_command("UNBLOCK_COMMAND")
BLOCKED_COMMAND = get_command("BLOCKED_COMMAND")


@app.on_message(filters.command(BLOCK_COMMAND) & SUDOERS)
@language
async def useradd(_client: Client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in BANNED_USERS:
            return await message.reply_text(_["block_1"].format(user.mention))
        await add_gban_user(user.id)
        BANNED_USERS.add(user.id)
        await message.reply_text(_["block_2"].format(user.mention))
        return
    if message.reply_to_message.from_user.id in BANNED_USERS:
        return await message.reply_text(
            _["block_1"].format(message.reply_to_message.from_user.mention)
        )
    await add_gban_user(message.reply_to_message.from_user.id)
    BANNED_USERS.add(message.reply_to_message.from_user.id)
    await message.reply_text(
        _["block_2"].format(message.reply_to_message.from_user.mention)
    )


@app.on_message(filters.command(UNBLOCK_COMMAND) & SUDOERS)
@language
async def userdel(_client: Client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in BANNED_USERS:
            return await message.reply_text(_["block_3"])
        await remove_gban_user(user.id)
        BANNED_USERS.remove(user.id)
        await message.reply_text(_["block_4"])
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in BANNED_USERS:
        return await message.reply_text(_["block_3"])
    await remove_gban_user(user_id)
    BANNED_USERS.remove(user_id)
    await message.reply_text(_["block_4"])


@app.on_message(filters.command(BLOCKED_COMMAND) & SUDOERS)
@language
async def sudoers_list(client: Client, message: Message, _):
    if not BANNED_USERS:
        return await message.reply_text(_["block_5"])
    mystic = await message.reply_text(_["block_6"])
    msg = _["block_7"]
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except Exception:
            continue
        msg += f"{count}➤ {user}\n"
    if count == 0:
        return await mystic.edit_text(_["block_5"])
    else:
        return await mystic.edit_text(msg)


__MODULE__ = "Lista de Ban"
__HELP__ = """
<b>✧ /blacklistchat</b> [ID do chat] - Bloqueia um chat de usar o Music Bot.
<b>✧ /whitelistchat</b> [ID do chat] - Remove um chat da lista de bloqueados, permitindo usar o Music Bot.
<b>✧ /blacklistedchat</b> - Verifica todos os chats bloqueados.

<b>✧ /block</b> [nome de usuário ou responder a um usuário] - Impede que um usuário use os comandos do bot.
<b>✧ /unblock</b> [nome de usuário ou responder a um usuário] - Remove um usuário da lista de bloqueados do bot.
<b>✧ /blockedusers</b> - Verifica a lista de usuários bloqueados.

<b>✧ /gban</b> [nome de usuário ou responder a um usuário] - Bane globalmente um usuário de todos os chats atendidos pelo bot e impede-o de usar seu bot.
<b>✧ /ungban</b> [nome de usuário ou responder a um usuário] - Remove um usuário da lista de banidos globalmente do bot e permite que ele use seu bot.
<b>✧ /gbannedusers</b> - Verifica a lista de usuários banidos globalmente.
"""
