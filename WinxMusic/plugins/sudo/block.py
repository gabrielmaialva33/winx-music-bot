from pyrogram import filters, Client
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import add_gban_user, remove_gban_user
from WinxMusic.utils.decorators.language import language
from config import BANNED_USERS
from strings import command, get_command

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
async def userdel(client, message: Message, _):
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
async def sudoers_list(client, message: Message, _):
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


__MODULE__ = "B-list"
__HELP__ = f"""
<b>✧ {command("BLACKLISTCHAT_COMMAND")}</b> [ID do chat] - Bloquear qualquer chat de usar o Bot de Música.
<b>✧ {command("WHITELISTCHAT_COMMAND")}</b> [ID do chat] - Desbloquear qualquer chat da lista de bloqueio para usar o Bot de Música.
<b>✧ {command("BLACKLISTEDCHAT_COMMAND")}</b> - Verificar todos os chats bloqueados.

<b>✧ {command("BLOCK_COMMAND")}</b> [Nome de usuário ou responder a um usuário] - Impede um usuário de usar comandos do bot.
<b>✧ {command("UNBLOCK_COMMAND")}</b> [Nome de usuário ou responder a um usuário] - Remove um usuário da lista de bloqueio do bot.
<b>✧ {command("BLOCKED_COMMAND")}</b> - Verificar a lista de usuários bloqueados.

<b>✧ {command("GBAN_COMMAND")}</b> [Nome de usuário ou responder a um usuário] - Banir um usuário de todos os chats atendidos e impedir que ele use seu bot.
<b>✧ {command("UNGBAN_COMMAND")}</b> [Nome de usuário ou responder a um usuário] - Remove um usuário da lista de banimento global e permite que ele use seu bot.
<b>✧ {command("GBANNED_COMMAND")}</b> - Verificar a lista de usuários banidos globalmente.
"""
