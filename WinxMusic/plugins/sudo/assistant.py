import os
from inspect import getfullargspec

from pyrogram import Client, filters
from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.database import get_client


@app.on_message(filters.command("setpfp", prefixes=".") & SUDOERS)
async def set_pfp(_client: Client, message: Message):
    from WinxMusic.core.userbot import assistants

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="Reply to a photo")
    for num in assistants:
        client = await get_client(num)
        photo = await message.reply_to_message.download()
        try:
            await client.set_profile_photo(photo=photo)
            await eor(message, text="Successfully Changed PFP.")
            os.remove(photo)
        except Exception as e:
            await eor(message, text=e)
            os.remove(photo)


@app.on_message(filters.command("setbio", prefixes=".") & SUDOERS)
async def set_bio(client: Client, message: Message):
    from WinxMusic.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text="Give some text to set as bio.")
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await eor(message, text="Changed Bio.")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(message, text="Give some text to set as bio.")


@app.on_message(filters.command("setname", prefixes=".") & SUDOERS)
async def set_name(client: Client, message: Message):
    from WinxMusic.core.userbot import assistants

    if len(message.command) == 1:
        return await eor(message, text="Give some text to set as name.")
    elif len(message.command) > 1:
        for num in assistants:
            client = await get_client(num)
            name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await eor(message, text=f"name Changed to {name} .")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(message, text="Give some text to set as name.")


@app.on_message(filters.command("delpfp", prefixes=".") & SUDOERS)
async def del_pfp(_client: Client, message: Message):
    from WinxMusic.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos(photos[0].file_id)
                await eor(message, text="Foto deletada com sucesso")
            else:
                await eor(message, text="Nenhuma foto de perfil encontrada.")
        except Exception as e:
            await eor(message, text=e)


@app.on_message(filters.command("delallpfp", prefixes=".") & SUDOERS)
async def delall_pfp(_client: Client, message: Message):
    from WinxMusic.core.userbot import assistants

    for num in assistants:
        client = await get_client(num)
        photos = [p async for p in client.get_chat_photos("me")]
        try:
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos[1:]])
                await eor(message, text="Fotos deletadas com sucesso")
            else:
                await eor(message, text="Nenhuma foto de perfil encontrada.")
        except Exception as e:
            await eor(message, text=e)


async def eor(message: Message, **kwargs):
    func = (
        (message.edit_text if message.from_user.is_self else message.reply)
        if message.from_user
        else message.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})


"""

<u>Comandos do Assistente:</u>
.setpfp - Responda em uma foto para definir a foto de perfil de todos os assistentes do bot [apenas foto] [somente para usuário sudo]

.setname [texto] - Para definir o nome de todos os assistentes [somente para usuário sudo]

.setbio [texto] - Para definir a bio de todos os assistentes [somente para usuário sudo]


.delpfp - Deletar a foto de perfil do assistente [apenas uma foto de perfil será deletada] [somente para usuário sudo]

.delallpfp - Deletar todas as fotos de perfil do assistente [apenas uma foto de perfil permanecerá] [somente para usuário sudo]

<u>Comandos do Assistente do Grupo:</u>

 /checkassistant - Verificar detalhes do seu assistente de grupo

 /setassistant - Alterar para um assistente específico para o seu grupo

 /changeassistant - Alterar o assistente do seu grupo para um assistente aleatório disponível nos servidores do bot

"""
