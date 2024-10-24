from pyrogram import Client
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultPhoto,
    InlineQuery,
)
from youtubesearchpython.__future__ import VideosSearch

from WinxMusic import app
from WinxMusic.utils.inlinequery import answer
from config import BANNED_USERS


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client: Client, query: InlineQuery):
    text = query.query.strip().lower()
    answers = []
    if text.strip() == "":
        try:
            await client.answer_inline_query(query.id, results=answer, cache_time=10)
        except:
            return
    else:
        a = VideosSearch(text, limit=20)
        result = (await a.next()).get("result")
        for x in range(15):
            title = (result[x]["title"]).title()
            duration = result[x]["duration"]
            views = result[x]["viewCount"]["short"]
            thumbnail = result[x]["thumbnails"][0]["url"].split("?")[0]
            channellink = result[x]["channel"]["link"]
            channel = result[x]["channel"]["name"]
            link = result[x]["link"]
            published = result[x]["publishedTime"]
            description = f"{views} | {duration} Minutos | {channel}  | {published}"
            buttons = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Assistir no YouTube",
                            url=link,
                        )
                    ],
                ]
            )
            searched_text = f"""
❇️**Título:** [{title}]({link})

⏳**Duração:** {duration} Minutos
👀**Visualizações:** `{views}`
⏰**Publicado em:** {published}
🎥**Nome do Canal:** {channel}
📎**Link do Canal:** [Visite aqui]({channellink})

__Responda com /play nesta mensagem pesquisada para reproduzir no chat de voz.__

⚡️ **Busca inline por {app.mention}**"""
            answers.append(
                InlineQueryResultPhoto(
                    photo_url=thumbnail,
                    title=title,
                    thumb_url=thumbnail,
                    description=description,
                    caption=searched_text,
                    reply_markup=buttons,
                )
            )
        try:
            return await client.answer_inline_query(query.id, results=answers)
        except:
            return
