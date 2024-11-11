from math import ceil
from typing import Dict

from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup

from WinxMusic import app, Platform, LOGGER
from WinxMusic.utils import get_lang
from WinxMusic.utils.stream.stream import stream
from config import BANNED_USERS, PREFIXES
from strings import get_command, get_string

MOVIES_COMMAND = get_command("MOVIES_COMMAND")
ANIME_COMMAND = get_command("ANIME_COMMAND")

RESULTS_PER_PAGE = 4

context_db: Dict[int, Dict] = {}


class ContextManager:
    """Handles storing and retrieving user-specific context."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_context(self) -> Dict:
        return context_db.get(self.user_id, {})

    def update_context(self, **kwargs):
        context = self.get_context()
        context.update(kwargs)
        context_db[self.user_id] = context

    def reset_context(self):
        context_db.pop(self.user_id, None)


@app.on_message(
    filters.command(MOVIES_COMMAND, prefixes=PREFIXES)
    & filters.group
    & ~BANNED_USERS
)
async def scan_movie_folder(_, message: Message):
    context_db.update({message.from_user.id: {}})
    query = (
        message.text.split(None, 1)[1].strip()
        if len(message.text.split()) > 1
        else (message.reply_to_message.text if message.reply_to_message else None)
    )
    if not query:
        return await message.reply_text("🎬 𝗜𝗻𝗳𝗼𝗿𝗺𝗲 𝗼 𝗳𝗶𝗹𝗺𝗲 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗯𝘂𝘀𝗰𝗮𝗿.")

    result = await Platform.animezey.search_movie(query)
    if not result:
        return await message.reply_text("<b>No results found.</b>")

    next_page_token = result.get('nextPageToken') or None
    cur_page_index = result.get('curPageIndex') or 0

    video_files = [
        file for file in result['data']['files']
        if file['mimeType'] in ('video/x-matroska', 'video/mp4')
    ]

    if not video_files:
        return await message.reply_text("<b>No video files found.</b>")

    context_manager = ContextManager(message.from_user.id)
    context_manager.update_context(query=query, page_token=next_page_token, page_index=cur_page_index,
                                   files=video_files)

    await send_results_page(message, message.from_user.id)

    await Platform.animezey.close()


@app.on_message(
    filters.command(ANIME_COMMAND, prefixes=PREFIXES)
    & filters.group
    & ~BANNED_USERS
)
async def scan_anime_folder(_, message: Message):
    context_db.update({message.from_user.id: {}})
    query = (
        message.text.split(None, 1)[1].strip()
        if len(message.text.split()) > 1
        else (message.reply_to_message.text if message.reply_to_message else None)
    )
    if not query:
        return await message.reply_text("🎬 𝗜𝗻𝗳𝗼𝗿𝗺𝗲 𝗼 𝗾𝘂𝗲 𝗱𝗲𝘀𝗲𝗷𝗮 𝗯𝘂𝘀𝗰𝗮𝗿.")

    result = await Platform.animezey.search_anime(query)
    if not result:
        return await message.reply_text("<b>No results found.</b>")

    next_page_token = result.get('nextPageToken') or None
    cur_page_index = result.get('curPageIndex') or 0

    video_files = [
        file for file in result['data']['files']
        if file['mimeType'] in ('video/x-matroska', 'video/mp4')
    ]

    if not video_files:
        return await message.reply_text("<b>No video files found.</b>")

    context_manager = ContextManager(message.from_user.id)
    context_manager.update_context(query=query, page_token=next_page_token, page_index=cur_page_index,
                                   files=video_files)

    await send_results_page(message, message.from_user.id)

    await Platform.animezey.close()


async def send_results_page(message: Message, user_id: int):
    context = context_db[user_id]
    files = context["files"]

    page_index = context["page_index"]
    total_pages = ceil(len(files) / RESULTS_PER_PAGE)

    start = page_index * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    files_on_page = files[start:end]

    text = f"🎥 <b>Filmes encontrados: {len(files)}</b> - Página {page_index + 1}/{total_pages}</b>\n\n"
    for idx, file in enumerate(files_on_page, start=1):
        name = file.get("name", "<b>Sem título</b>")
        # type = file.get("mimeType", None)
        link = file.get("link", "#")
        text += f"<b>📽️ {idx} - <a href='{Platform.animezey.base_url + link}'>{name}</a></b>\n"

    buttons = [
        InlineKeyboardButton(f"Ver {idx}", callback_data=f"view_{page_index}_{idx}")
        for idx in range(1, len(files_on_page) + 1)
    ]
    button_pairs = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

    navigation_buttons = [
        InlineKeyboardButton("⬅️", callback_data="prev_page") if page_index > 0 else None,
        InlineKeyboardButton("➡️", callback_data="next_page") if page_index < total_pages - 1 else None,
    ]
    button_pairs.append(list(filter(None, navigation_buttons)))
    button_pairs.append([InlineKeyboardButton("❌ Cancelar", callback_data="alpha_cancel")])

    markup = InlineKeyboardMarkup(button_pairs)

    # markup = InlineKeyboardMarkup(
    #     [
    #         [
    #             (
    #                 InlineKeyboardButton("⬅️", callback_data="prev_page")
    #                 if page_index > 0
    #                 else None
    #             ),
    #             (
    #                 InlineKeyboardButton("➡️", callback_data="next_page")
    #                 if page_index < total_pages - 1
    #                 else None
    #             ),
    #         ],
    #         [InlineKeyboardButton("❌", callback_data="alpha_cancel")],
    #     ]
    # )

    # markup.inline_keyboard = [list(filter(None, row)) for row in markup.inline_keyboard]

    # await message.reply_text(text, reply_markup=markup)

    await message.reply_text(text, reply_markup=markup)


@app.on_callback_query(filters.regex(r"^alpha_cancel$"))
async def cancel_alpha(_client: Client, callback_query: CallbackQuery):
    context_db.pop(callback_query.from_user.id, None)
    await callback_query.message.delete()


@app.on_callback_query(filters.regex(r"^(prev|next)_page$"))
async def paginate_results(_client: Client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    action = callback_query.data.split("_")[0]

    context = context_db[user_id]

    if action == "prev":
        context["page_index"] -= 1
    elif action == "next":
        context["page_index"] += 1

    await callback_query.message.delete()
    await send_results_page(callback_query.message, user_id)


@app.on_callback_query(filters.regex(r"^view_\d+_\d+$"))
async def view_movie(_client: Client, callback_query: CallbackQuery):
    language = await get_lang(callback_query.message.chat.id)
    _ = get_string(language)

    user_id = callback_query.from_user.id
    page_index, idx = map(int, callback_query.data.split("_")[1:])

    context = context_db[user_id]
    files = context["files"]

    file = files[page_index * RESULTS_PER_PAGE + idx - 1]
    name = file.get("name", "<b>Sem título</b>")
    link = file.get("link", "#")

    if await Platform.animezey.download(name, link, callback_query.message):
        dur = await Platform.animezey.get_duration(name)
        file_path = await Platform.animezey.get_filepath(name)
        details = {
            "title": name,
            "dur": dur,
            "path": file_path,
            "link": link,
        }

    try:
        await stream(
            _,
            mystic=callback_query.message,
            user_id=user_id,
            result=details,
            chat_id=callback_query.message.chat.id,
            user_name=callback_query.from_user.first_name,
            original_chat_id=callback_query.message.chat.id,
            streamtype="animezey",
        )
    except Exception as e:
        ex_type = type(e).__name__
        if ex_type == "AssistantErr":
            err = e
        else:
            err = _["general_3"].format(ex_type)
            LOGGER(__name__).error("An error occurred", exc_info=True)
        return await callback_query.message.edit(err)
    return await callback_query.message.delete()


class EqInlineKeyboardButton(InlineKeyboardButton):
    """
    This class is used to compare InlineKeyboardButton objects.
    """

    def __eq__(self, other: InlineKeyboardButton):
        return self.text == other.text

    def __lt__(self, other: InlineKeyboardButton):
        return self.text < other.text

    def __gt__(self, other: InlineKeyboardButton):
        return self.text > other.text
