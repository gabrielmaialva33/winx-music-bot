import asyncio

from pyrogram import enums
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait

from WinxMusic import app

# ------------------------------------------------------------------------------- #

chatQueue = []

stopProcess = False


# ------------------------------------------------------------------------------- #

@app.on_message(filters.command(["zombies", "clean"]))
async def remove(_, message):
    global stopProcess
    try:
        try:
            sender = await app.get_chat_member(message.chat.id, message.from_user.id)
            has_permissions = sender.privileges
        except:
            has_permissions = message.sender_chat
        if has_permissions:
            bot = await app.get_chat_member(message.chat.id, "self")
            if bot.status == ChatMemberStatus.MEMBER:
                await message.reply("➠ | Você precisa me tornar administrador para usar este comando.")
            else:
                if len(chatQueue) > 30:
                    await message.reply(
                        "➠ | Eu não posso executar este comando em mais de 30 chats ao mesmo tempo.")
                else:
                    if message.chat.id in chatQueue:
                        await message.reply(
                            "➠ | Este chat já está na fila de limpeza. Aguarde até que o processo seja concluído. "
                            "Digite /stop para parar o processo.")
                    else:
                        chatQueue.append(message.chat.id)
                        deletedList = []
                        async for member in app.get_chat_members(message.chat.id):
                            if member.user.is_deleted:
                                deletedList.append(member.user)
                            else:
                                pass
                        lenDeletedList = len(deletedList)
                        if lenDeletedList == 0:
                            await message.reply("⟳ | Sem contas excluídas detectadas neste chat.")
                            chatQueue.remove(message.chat.id)
                        else:
                            k = 0
                            processTime = lenDeletedList * 1
                            temp = await app.send_message(message.chat.id,
                                                          f" 🧭 | Total de {lenDeletedList} contas excluídas "
                                                          f"detectadas.\n🥀 | Tempo estimado: {processTime} segundos "
                                                          f"a partir de agora.")
                            if stopProcess: stopProcess = False
                            while len(deletedList) > 0 and not stopProcess:
                                deletedAccount = deletedList.pop(0)
                                try:
                                    await app.ban_chat_member(message.chat.id, deletedAccount.id)
                                except Exception:
                                    pass
                                k += 1
                                await asyncio.sleep(10)
                            if k == lenDeletedList:
                                await message.reply(f" ✅ | Sucesso! {k} contas excluídas foram removidas deste chat.")
                                await temp.delete()
                            else:
                                await message.reply(f" ✅ | Sucesso! {k} contas excluídas foram removidas deste chat.")
                                await temp.delete()
                            chatQueue.remove(message.chat.id)
        else:
            await message.reply("👮🏻 | Você não tem permissão para usar este comando.")
    except FloodWait as e:
        await asyncio.sleep(e.value)

    # ------------------------------------------------------------------------------- #


@app.on_message(filters.command(["adms"]))
async def admins(_, message):
    try:
        adminList = []
        ownerList = []
        async for admin in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not admin.privileges.is_anonymous:
                if admin.user.is_bot:
                    pass
                elif admin.status == ChatMemberStatus.OWNER:
                    ownerList.append(admin.user)
                else:
                    adminList.append(admin.user)
            else:
                pass
        lenAdminList = len(ownerList) + len(adminList)
        text2 = f"**Fodas do Grupo - {message.chat.title}**\n\n"
        try:
            owner = ownerList[0]
            if owner.username is None:
                text2 += f"👑 Dono\n└ {owner.mention}\n\n👮🏻 Adm\n"
            else:
                text2 += f"👑 Dono\n└ @{owner.username}\n\n👮🏻 Adm\n"
        except:
            text2 += f"👑 Dono\n└ <i>Hidden</i>\n\n👮🏻 Adm\n"
        if len(adminList) == 0:
            text2 += "└ <i>Dono Escondidos</i>"
            await app.send_message(message.chat.id, text2)
        else:
            while len(adminList) > 1:
                admin = adminList.pop(0)
                if admin.username is None:
                    text2 += f"├ {admin.mention}\n"
                else:
                    text2 += f"├ @{admin.username}\n"
            else:
                admin = adminList.pop(0)
                if admin.username is None:
                    text2 += f"└ {admin.mention}\n\n"
                else:
                    text2 += f"└ @{admin.username}\n\n"
            text2 += f"✅ | **Total de adms**: {lenAdminList}"
            await app.send_message(message.chat.id, text2)
    except FloodWait as e:
        await asyncio.sleep(e.value)

    # ------------------------------------------------------------------------------- #


@app.on_message(filters.command("bots"))
async def bots(_, message):
    try:
        botList = []
        async for bot in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.BOTS):
            botList.append(bot.user)
        lenBotList = len(botList)
        text3 = f"**Lista de bot - {message.chat.title}**\n\n🤖 bots\n"
        while len(botList) > 1:
            bot = botList.pop(0)
            text3 += f"├ @{bot.username}\n"
        else:
            bot = botList.pop(0)
            text3 += f"└ @{bot.username}\n\n"
            text3 += f"✅ | *Total de bos**: {lenBotList}"
            await app.send_message(message.chat.id, text3)
    except FloodWait as e:
        await asyncio.sleep(e.value)

# ------------------------------------------------------------------------------- #
