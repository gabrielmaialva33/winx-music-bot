from pyrogram.types import Message

from WinxMusic import app
from WinxMusic.utils.database import is_on_off
from config import LOG, LOG_GROUP_ID


async def play_logs(message: Message, streamtype: str):
    if await is_on_off(LOG):
        if message.chat.username:
            chatusername = f"@{message.chat.username}"
        else:
            chatusername = "🔒 Grupo Privado"

        logger_text = f"""
🎵 **Registro de Reprodução - {app.mention}** 🎵

📌 **ID do Chat:** `{message.chat.id}`
🏷️ **Nome do Chat:** {message.chat.title}
🔗 **Nome de Usuário do Chat:** {chatusername}

👤 **ID do Usuário:** `{message.from_user.id}`
📛 **Nome:** {message.from_user.mention}
📱 **Nome de Usuário:** @{message.from_user.username}

🔍 **Consulta:** {message.text.split(None, 1)[1]}
🎧 **Tipo de Transmissão:** {streamtype}"""

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
