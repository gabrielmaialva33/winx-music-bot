from WinxMusic import app
from WinxMusic.utils.database import is_on_off
from config import LOG, LOG_GROUP_ID


async def play_logs(message, streamtype):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "grupo privado"

        logger_text = f"""
**{app.mention} registro de reprodução**

**ID do chat:** `{message.chat.id}`
**Nome do chat:** {message.chat.title}
**Nome de usuário do chat:** {chatusername}

**ID do usuário:** `{message.from_user.id}`
**Nome:** {message.from_user.mention}
**Nome de usuário:** @{message.from_user.username}

**Consulta:** {message.text.split(None, 1)[1]}
**Tipo de stream:** {streamtype}"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(e)
        return
