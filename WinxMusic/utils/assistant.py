from WinxMusic.utils.database import get_client


async def get_assistant_details():
    ms = ""
    msg = "**Uso** : /setassistant [número do assistente] para alterar e definir manualmente o assistente do grupo \n Abaixo estão alguns detalhes de assistentes disponíveis\n"
    try:
        a = await get_client(1)
        msg += f"Número do assistente: `1` \nNome: [{a.name}](https://t.me/{a.username})  \nNome de usuário: @{a.username} \nID: {a.id}\n\n"
    except:
        pass

    try:
        b = await get_client(2)
        msg += f"Número do assistente: `2` \nNome: [{b.name}](https://t.me/{b.username})  \nNome de usuário: @{b.username} \nID: {b.id}\n"
    except:
        pass

    try:
        c = await get_client(3)
        msg += f"Número do assistente: `3` \nNome: [{c.name}](https://t.me/{c.username})  \nNome de usuário: @{c.username} \nID: {c.id}\n"
    except:
        pass

    try:
        d = await get_client(4)
        msg += f"Número do assistente: `4` \nNome: [{d.name}](https://t.me/{d.username})  \nNome de usuário: @{d.username} \nID: {d.id}\n"
    except:
        pass

    try:
        e = await get_client(5)
        msg += f"Número do assistente: `5`\nNome: [{e.name}](https://t.me/{e.username})\nNome de usuário: @{e.username} \nID: {e.id}\n"
    except:
        pass

    return msg


async def is_avl_assistant():
    from config import STRING1, STRING2, STRING3, STRING4, STRING5

    filled_count = sum(
        1
        for var in [STRING1, STRING2, STRING3, STRING4, STRING5]
        if var and var.strip()
    )
    if filled_count == 1:
        return True
    else:
        return False
