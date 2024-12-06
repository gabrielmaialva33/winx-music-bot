import asyncio
import json
import os
import random
import re
import string
import time
from datetime import datetime, timedelta
from typing import Optional, TypedDict, List, Dict, Union, Any

import aiohttp
from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    Message,
)

from WinxMusic import app
from WinxMusic.utils import get_readable_time, convert_bytes

downloader = {}


class FileDict(TypedDict):
    mimeType: str
    name: str
    modifiedTime: str
    id: str
    driveId: str
    link: str


class SearchMovieResponse(TypedDict):
    nextPageToken: Optional[str]
    curPageIndex: int
    data: "DataDict"


class DataDict(TypedDict):
    nextPageToken: Optional[str]
    files: List[FileDict]


class AnimeZey:
    def __init__(self):
        self.base_url: str = "https://animezey16082023.animezey16082023.workers.dev"
        self.session: Optional[aiohttp.ClientSession] = None
        self.session_headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
            "Content-Type": "application/json",
        }
        self.timeout: int = 60
        self.sleep = 5

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self.session_headers)
        return self.session

    async def request(
            self, endpoint: str, method: str, data: Optional[Dict[str, Any]] = None
    ) -> Union[Dict[str, Any], str, None]:
        session = await self._get_session()
        try:
            async with session.request(
                    method, f"{self.base_url}{endpoint}", json=data
            ) as response:
                response.raise_for_status()
                content_type = response.headers.get("Content-Type", "")
                if "application/json" in content_type:
                    return await response.json()
                else:
                    text = await response.text()
                    try:
                        return json.loads(text)
                    except json.JSONDecodeError:
                        return text
        except aiohttp.ClientError as e:
            print(f"Request failed: {e}")
            return None

    async def search_anime(
            self, query: str, page_token: Optional[str] = None
    ) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/0:search", "POST", {"q": query, "page_token": page_token, "page_index": 0}
        )

    async def search_movie(
            self, query: str, page_token: Optional[str] = None
    ) -> Optional[SearchMovieResponse]:
        response: Union[Dict[str, Any], str, None] = await self.request(
            "/1:search",
            "POST",
            {
                "q": query,
                "page_token": page_token,
                "page_index": 0,
            },
        )
        if isinstance(response, dict):
            return response
        return None

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def download(self, file_name: str, link: str, mystic: Message) -> bool:
        download_id = "".join(random.choices(string.ascii_letters + string.digits, k=8))
        user_id = mystic.from_user.id

        sanitized_file_name: str = re.sub(r'[\/\?<>\\:\*\|"]', "_", file_name)
        file_path: str = f"downloads/{sanitized_file_name}"

        left_time = {}
        speed_counter = {}

        if os.path.exists(file_path):
            return True

        session = await self._get_session()

        async def download_file():
            async def progress(current, total):
                if current == total:
                    return
                current_time = time.time()
                start_time = speed_counter.get("start")
                check_time = current_time - start_time
                upl = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="🚦 Cancelar Download",
                                callback_data=f"stop_downloading_animezey_{download_id}",
                            ),
                        ]
                    ]
                )
                if datetime.now() > left_time.get("update_time", datetime.min):
                    percentage = current * 100 / total
                    percentage = str(round(percentage, 2))
                    speed = current / check_time
                    eta = int((total - current) / speed)
                    downloader[download_id] = task
                    downloader["eta"] = eta
                    eta = get_readable_time(eta)
                    if not eta:
                        eta = "0 seg"
                    total_size = convert_bytes(total)
                    completed_size = convert_bytes(current)
                    speed = convert_bytes(speed)
                    text = f"""
    **AnimeZey Downloader 📥**

    💾 **Tamanho total do arquivo:** {total_size}
    ✅ **Concluído:** {completed_size} 
    📊 **Progresso:** {percentage[:5]}%

    ⚡ **Velocidade:** {speed}/s
    ⏳ **Tempo restante:** {eta}"""
                    try:
                        await mystic.edit_text(text, reply_markup=upl)
                    except Exception as e:
                        print(e)
                    left_time["update_time"] = datetime.now() + timedelta(
                        seconds=self.sleep
                    )

            speed_counter["start"] = time.time()
            left_time["update_time"] = datetime.now()

            try:
                async with session.get(f"{self.base_url}{link}") as response:
                    response.raise_for_status()
                    total_size = int(response.headers.get("Content-Length", 0))
                    chunk_size = 1024 * 1024  # 1MB

                    with open(file_path, "wb") as file:
                        current_size = 0
                        async for chunk in response.content.iter_chunked(chunk_size):
                            file.write(chunk)
                            current_size += len(chunk)
                            await progress(current_size, total_size)

                    await mystic.edit_text(
                        "✅ Download concluído com sucesso...\n📂 Processando arquivo agora"
                    )
                    downloader.pop("eta", None)
                    downloader.pop(download_id, None)
                    return True
            except Exception as e:
                await mystic.edit_text(f"Erro ao baixar: {str(e)}")
                return False

        if len(downloader) > 10:
            timers = [downloader[x] for x in downloader if x != "eta"]
            try:
                low = min(timers)
                eta = get_readable_time(low)
            except Exception:
                eta = "Desconhecido"
            await mystic.edit_text(
                f"Muitos downloads simultâneos! Tempo estimado de espera: {eta}."
            )
            return False

        task = asyncio.create_task(
            download_file(), name=f"download_{sanitized_file_name}"
        )
        downloader[download_id] = task
        await task
        downloaded = downloader.get("eta")
        if downloaded:
            downloader.pop("eta", None)
            return False
        return True

    async def movie_folder(self) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/1:/Filmes/",
            "POST",
            {
                "id": "",
                "type": "folder",
                "password": "",
                "page_token": "",
                "page_index": 0,
            },
        )

    async def navigate_folder(self, folder_id: str) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/1:/Filmes/",
            "POST",
            {
                "id": folder_id,
                "type": "folder",
                "password": "",
                "page_token": "",
                "page_index": 0,
            },
        )

    async def get_duration(self, file_path: str) -> int:
        print(f"Getting duration for: {file_path}")
        try:
            duration = 0
            process = await asyncio.create_subprocess_exec(
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await process.communicate()
            duration = int(float(stdout))
        except Exception as e:
            print(f"Error getting duration: {e}")
            duration = 0
        return duration

    async def get_filepath(self, file_name: str) -> str:
        sanitized_file_name: str = re.sub(r'[\/\?<>\\:\*\|"]', "_", file_name)
        file_path = os.path.join(os.path.realpath("downloads"), sanitized_file_name)
        return file_path


@app.on_callback_query(
    filters.regex(pattern=r"^stop_downloading_animezey_([a-zA-Z0-9]+)")
)
async def stop_downloading_animezey(_, callback_query: CallbackQuery):
    download_id = callback_query.data.split("_")[3]

    task = downloader.get(download_id)
    if task:
        task.cancel()
        downloader.pop(download_id, None)

    # todo remove file if exists?

    await callback_query.edit_message_text("🚦 Download cancelado com sucesso.")
