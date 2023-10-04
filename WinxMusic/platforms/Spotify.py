import re

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch

import config


class SpotifyAPI:
    def __init__(self):
        self.regex = r"^(https:\/\/open.spotify.com\/)(.*)$"
        self.client_id = config.SPOTIFY_CLIENT_ID
        self.client_secret = config.SPOTIFY_CLIENT_SECRET
        if self.client_id and self.client_secret:
            self.client_credentials_manager = SpotifyClientCredentials(self.client_id, self.client_secret)
            self.spotify = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        else:
            self.spotify = None

    async def valid(self, link: str):
        return bool(re.search(self.regex, link))

    async def track(self, link: str):
        track = self.spotify.track(link)
        info = track["name"]
        artists = [artist["name"] for artist in track["artists"] if "Various Artists" not in artist["name"]]
        info += " ".join(artists)
        results = VideosSearch(info, limit=1, language="en", region="US")
        result = (await results.next())["result"][0]
        ytlink = result["link"]
        title = result["title"]
        vidid = result["id"]
        duration_min = result["duration"]
        thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": ytlink,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def playlist(self, url):
        playlist = self.spotify.playlist(url)
        playlist_id = playlist["id"]
        results = []
        for item in playlist["tracks"]["items"]:
            music_track = item["track"]
            info = music_track["name"]
            artists = [artist["name"] for artist in music_track["artists"] if "Various Artists" not in artist["name"]]
            info += " ".join(artists)
            results.append(info)
        return results, playlist_id

    async def album(self, url):
        album = self.spotify.album(url)
        album_id = album["id"]
        results = []
        for item in album["tracks"]["items"]:
            info = item["name"]
            artists = [artist["name"] for artist in item["artists"] if "Various Artists" not in artist["name"]]
            info += " ".join(artists)
            results.append(info)
        return results, album_id

    async def artist(self, url):
        artistinfo = self.spotify.artist(url)
        artist_id = artistinfo["id"]
        results = []
        artisttoptracks = self.spotify.artist_top_tracks(url)
        for item in artisttoptracks["tracks"]:
            info = item["name"]
            artists = [artist["name"] for artist in item["artists"] if "Various Artists" not in artist["name"]]
            info += " ".join(artists)
            results.append(info)
        return results, artist_id
