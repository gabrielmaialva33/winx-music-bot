import json
import re
from typing import Optional, TypedDict, List, Dict, Union, Any

import aiohttp


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

    async def _get_session(self) -> aiohttp.ClientSession:
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(headers=self.session_headers)
        return self.session

    async def request(self, endpoint: str, method: str, data: Optional[Dict[str, Any]] = None) -> Union[
        Dict[str, Any], str, None]:
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

    async def search_anime(self, query: str, page_token: Optional[str] = None) -> Union[Dict[str, Any], str, None]:
        return await self.request(
            "/0:search", "POST", {"q": query, "page_token": page_token, "page_index": 0}
        )

    async def search_movie(self, query: str, page_token: Optional[str] = None) -> Optional[SearchMovieResponse]:
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

    async def download(self, file_name: str, link: str) -> str:
        sanitized_file_name: str = re.sub(r'[\/\?<>\\:\*\|"]', "_", file_name)
        file_path: str = f"movies/{sanitized_file_name}"
        session = await self._get_session()

        try:
            async with session.get(f"{self.base_url}{link}") as response:
                response.raise_for_status()
                with open(file_path, "wb") as f:
                    f.write(await response.read())
            return file_path
        except aiohttp.ClientError as e:
            print(f"Download failed: {e}")
            return ""

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
