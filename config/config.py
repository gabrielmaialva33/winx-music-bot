import re
import sys
from os import getenv

from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get it from my.telegram.org

API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")

## Get it from @Botfather in Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

# Database to save your chats and stats... Get MongoDB:-  https://telegra.ph/How-To-get-Mongodb-URI-04-06
MONGO_DB_URI = getenv("MONGO_DB_URI", None)

CLEANMODE_DELETE_MINS = int(
    getenv("CLEANMODE_MINS", "5")
)  # Remember to give value in Seconds

# Custom max audio(music) duration for voice chat. set DURATION_LIMIT in variables with your own time(mins), Default to 60 mins.

DURATION_LIMIT_MIN = int(
    getenv("DURATION_LIMIT", "300")
)  # Remember to give value in Minutes

EXTRA_PLUGINS = getenv(
    "EXTRA_PLUGINS",
    "False",
)

# Fill True if you want to load extra plugins


EXTRA_PLUGINS_REPO = getenv(
    "EXTRA_PLUGINS_REPO",
    "https://github.com/gabrielmaialva33/winx-extra-plugin",
)
# Fill here the external plugins repo where plugins that you want to load


EXTRA_PLUGINS_FOLDER = getenv("EXTRA_PLUGINS_FOLDER", "plugins")

# Your folder name in your extra plugins repo where all plugins stored


# Duration Limit for downloading Songs in MP3 or MP4 format from bot
SONG_DOWNLOAD_DURATION = int(
    getenv("SONG_DOWNLOAD_DURATION_LIMIT", "240")
)  # Remember to give value in Minutes

# You'll need a Private Group ID for this.
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "-1001285436101"))

# Fill in seconds if assistant is muted in voice chat assistant will leave  voice chat after the MUTE_WARNING_TIME

MUTE_WARNING_TIME = int(getenv("MUTE_WARNING_TIME", 100))

# Your User ID.
OWNER_ID = list(
    map(int, getenv("OWNER_ID", "7154724576").split())
)  # Input type must be interger

# make your bots privacy from telegra.ph and put your url here

PRIVACY_LINK = getenv(
    "PRIVACY_LINK", "https://telegra.ph/Privacy-Policy-for-WinxMusic-08-30"
)

# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

# You have to Enter the app name which you gave to identify your  Music Bot in Heroku.
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")

# For customized or modified Repository
UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/gabrielmaialva33/winx-music-bot",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

# GIT TOKEN ( if your edited repo is private)
GIT_TOKEN = getenv(
    "GIT_TOKEN",
    "",
)

# Only  Links formats are  accepted for this Var value.
SUPPORT_CHANNEL = getenv(
    "SUPPORT_CHANNEL", "https://t.me/winxbotx"
)  # Example:- https://t.me/winxbotx
SUPPORT_GROUP = getenv(
    "SUPPORT_GROUP", "https://t.me/winxmusicsupport"
)  # Example:- https://t.me/winxmusicsupport

# Set it in True if you want to leave your assistant after a certain amount of time. [Set time via AUTO_LEAVE_ASSISTANT_TIME]
AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", False)

# Time after which you're assistant account will leave chats automatically.
AUTO_LEAVE_ASSISTANT_TIME = int(
    getenv("ASSISTANT_LEAVE_TIME", 180)
)  # Remember to give value in Seconds

# Set it true if you want your bot to be private only [You'll need to allow CHAT_ID via /authorize command then only your bot will play music in that chat.]
PRIVATE_BOT_MODE = getenv("PRIVATE_BOT_MODE", "False")

# Time sleep duration For Youtube Downloader
YOUTUBE_DOWNLOAD_EDIT_SLEEP = int(getenv("YOUTUBE_EDIT_SLEEP", "3"))

# Time sleep duration For Telegram Downloader
TELEGRAM_DOWNLOAD_EDIT_SLEEP = int(getenv("TELEGRAM_EDIT_SLEEP", "5"))

# Your Github Repo.. Will be shown on /start Command
GITHUB_REPO = getenv(
    "GITHUB_REPO", "https://github.com/gabrielmaialva33/winx-music-bot"
)

# Spotify Client.. Get it from https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "fed42460adc148fab5beb47474b6cb8e")
SPOTIFY_CLIENT_SECRET = getenv(
    "SPOTIFY_CLIENT_SECRET", "d1cd09bfff114580b41d3ef845e314b6"
)

# Maximum number of video calls allowed on bot. You can later set it via /set_video_limit on telegram
VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "999"))

# Maximum Limit Allowed for users to save playlists on bot's server
SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "25"))

# MaximuM limit for fetching playlist's track from youtube, spotify, apple links.
PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "25"))

# Telegram audio  and video file size limit

TG_AUDIO_FILESIZE_LIMIT = int(
    getenv("TG_AUDIO_FILESIZE_LIMIT", "1073741824")
)  # Remember to give value in bytes

TG_VIDEO_FILESIZE_LIMIT = int(
    getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824")
)  # Remember to give value in bytes

# Chceckout https://www.gbmb.org/mb-to-bytes  for converting mb to bytes


# If you want your bot to setup the commands automatically in the bot's menu set it to true.
# Refer to https://i.postimg.cc/Bbg3LQTG/image.png
SET_CMDS = getenv("SET_CMDS", "False")

# You'll need a Pyrogram String Session for these vars. Generate String from our session generator bot or Userbot.
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)
STRING6 = getenv("STRING_SESSION6", None)
STRING7 = getenv("STRING_SESSION7", None)
STRING8 = getenv("STRING_SESSION8", None)
STRING9 = getenv("STRING_SESSION9", None)
STRING10 = getenv("STRING_SESSION10", None)

# Configs
BANNED_USERS = filters.user()
YTDOWNLOADER = 1
LOG = 2
LOG_FILE_NAME = "WinxLogs.txt"
TEMP_DB_FOLDER = "tempdb"
adminlist = {}
lyrical = {}
chatstats = {}
userstats = {}
clean = {}

autoclean = []

# Images

START_IMG_URL = getenv(
    "START_IMG_URL",
    "https://telegra.ph/file/0a1543a753bd665f015b2.jpg",
)

PING_IMG_URL = getenv(
    "PING_IMG_URL",
    "https://64.media.tumblr.com/ea7bbbc05fe47c0306c2ac389eccc252/7724188deed06fee-a2/s1280x1920/3e5de4c6847843b79902a50a0873a58325551d55.gifv",
)

PLAYLIST_IMG_URL = getenv(
    "PLAYLIST_IMG_URL",
    "https://64.media.tumblr.com/73084dccbeffd73655bb3a07cef7904a/ca2e3db2a56b2f2d-71/s540x810/747f6f9a572be30f47bb428e51aa66d9c2435b35.gifv",
)

GLOBAL_IMG_URL = getenv(
    "GLOBAL_IMG_URL",
    "https://64.media.tumblr.com/ac0bd0dbb6d9e3c7471630584e58b668/42dbca30b09f38f4-36/s1280x1920/ec602883a8242946698b201505bc7a47ac2f6afe.gifv",
)

STATS_IMG_URL = getenv(
    "STATS_IMG_URL",
    "https://64.media.tumblr.com/a98891c693052dd873231ab51b721421/d6aa089c4433b10c-24/s1280x1920/1d296936e8fa25471b51761e64fbeeaf0c28fc8a.gifv",
)

TELEGRAM_AUDIO_URL = getenv(
    "TELEGRAM_AUDIO_URL",
    "https://64.media.tumblr.com/79bb5c54237323c17c93af4c3c83671b/667b875d0810726a-86/s1280x1920/018a7062497c7599991eac83a4f41844484e90e7.gifv",
)

TELEGRAM_VIDEO_URL = getenv(
    "TELEGRAM_VIDEO_URL",
    "https://64.media.tumblr.com/79bb5c54237323c17c93af4c3c83671b/667b875d0810726a-86/s1280x1920/018a7062497c7599991eac83a4f41844484e90e7.gifv",
)

STREAM_IMG_URL = getenv(
    "STREAM_IMG_URL",
    "https://64.media.tumblr.com/ea7bbbc05fe47c0306c2ac389eccc252/7724188deed06fee-a2/s1280x1920/3e5de4c6847843b79902a50a0873a58325551d55.gifv",
)

SOUNCLOUD_IMG_URL = getenv(
    "SOUNCLOUD_IMG_URL",
    "https://64.media.tumblr.com/ea7bbbc05fe47c0306c2ac389eccc252/7724188deed06fee-a2/s1280x1920/3e5de4c6847843b79902a50a0873a58325551d55.gifv",
)

YOUTUBE_IMG_URL = getenv(
    "YOUTUBE_IMG_URL",
    "https://64.media.tumblr.com/c39b07d55fbdff89661056be8bd08dbd/df2251522787e803-87/s1280x1920/40ae16b0ab0adadc2914146b115ab4ba0480863e.gifv",
)

SPOTIFY_ARTIST_IMG_URL = getenv(
    "SPOTIFY_ARTIST_IMG_URL",
    "https://64.media.tumblr.com/73084dccbeffd73655bb3a07cef7904a/ca2e3db2a56b2f2d-71/s1280x1920/173c28fc197aef873f69df081e0671c35eacc9fb.gifv",
)

SPOTIFY_ALBUM_IMG_URL = getenv(
    "SPOTIFY_ALBUM_IMG_URL",
    "https://64.media.tumblr.com/73084dccbeffd73655bb3a07cef7904a/ca2e3db2a56b2f2d-71/s1280x1920/173c28fc197aef873f69df081e0671c35eacc9fb.gifv",
)

SPOTIFY_PLAYLIST_IMG_URL = getenv(
    "SPOTIFY_PLAYLIST_IMG_URL",
    "https://64.media.tumblr.com/73084dccbeffd73655bb3a07cef7904a/ca2e3db2a56b2f2d-71/s1280x1920/173c28fc197aef873f69df081e0671c35eacc9fb.gifv",
)


def time_to_seconds(time):
    string_time = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(string_time.split(":"))))


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))
SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

if SUPPORT_CHANNEL:
    if not re.match("(?:http|https)://", SUPPORT_CHANNEL):
        print(
            "[ERROR] - Your SUPPORT_CHANNEL url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if SUPPORT_GROUP:
    if not re.match("(?:http|https)://", SUPPORT_GROUP):
        print(
            "[ERROR] - Your SUPPORT_GROUP url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if UPSTREAM_REPO:
    if not re.match("(?:http|https)://", UPSTREAM_REPO):
        print(
            "[ERROR] - Your UPSTREAM_REPO url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if GITHUB_REPO:
    if not re.match("(?:http|https)://", GITHUB_REPO):
        print(
            "[ERROR] - Your GITHUB_REPO url is wrong. Please ensure that it starts with https://"
        )
        sys.exit()

if PING_IMG_URL:
    if (
        PING_IMG_URL
        != "https://64.media.tumblr.com/ea7bbbc05fe47c0306c2ac389eccc252/7724188deed06fee-a2/s1280x1920/3e5de4c6847843b79902a50a0873a58325551d55.gifv"
    ):
        if not re.match("(?:http|https)://", PING_IMG_URL):
            print(
                "[ERROR] - Your PING_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if PLAYLIST_IMG_URL:
    if (
        PLAYLIST_IMG_URL
        != "https://64.media.tumblr.com/73084dccbeffd73655bb3a07cef7904a/ca2e3db2a56b2f2d-71/s540x810/747f6f9a572be30f47bb428e51aa66d9c2435b35.gifv"
    ):
        if not re.match("(?:http|https)://", PLAYLIST_IMG_URL):
            print(
                "[ERROR] - Your PLAYLIST_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if GLOBAL_IMG_URL:
    if (
        GLOBAL_IMG_URL
        != "https://64.media.tumblr.com/ac0bd0dbb6d9e3c7471630584e58b668/42dbca30b09f38f4-36/s1280x1920/ec602883a8242946698b201505bc7a47ac2f6afe.gifv"
    ):
        if not re.match("(?:http|https)://", GLOBAL_IMG_URL):
            print(
                "[ERROR] - Your GLOBAL_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if STATS_IMG_URL:
    if (
        STATS_IMG_URL
        != "https://64.media.tumblr.com/a98891c693052dd873231ab51b721421/d6aa089c4433b10c-24/s1280x1920/1d296936e8fa25471b51761e64fbeeaf0c28fc8a.gifv"
    ):
        if not re.match("(?:http|https)://", STATS_IMG_URL):
            print(
                "[ERROR] - Your STATS_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if TELEGRAM_AUDIO_URL:
    if (
        TELEGRAM_AUDIO_URL
        != "https://64.media.tumblr.com/79bb5c54237323c17c93af4c3c83671b/667b875d0810726a-86/s1280x1920/018a7062497c7599991eac83a4f41844484e90e7.gifv"
    ):
        if not re.match("(?:http|https)://", TELEGRAM_AUDIO_URL):
            print(
                "[ERROR] - Your TELEGRAM_AUDIO_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if STREAM_IMG_URL:
    if (
        STREAM_IMG_URL
        != "https://64.media.tumblr.com/ea7bbbc05fe47c0306c2ac389eccc252/7724188deed06fee-a2/s1280x1920/3e5de4c6847843b79902a50a0873a58325551d55.gifv"
    ):
        if not re.match("(?:http|https)://", STREAM_IMG_URL):
            print(
                "[ERROR] - Your STREAM_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if SOUNCLOUD_IMG_URL:
    if (
        SOUNCLOUD_IMG_URL
        != "https://64.media.tumblr.com/ea7bbbc05fe47c0306c2ac389eccc252/7724188deed06fee-a2/s1280x1920/3e5de4c6847843b79902a50a0873a58325551d55.gifv"
    ):
        if not re.match("(?:http|https)://", SOUNCLOUD_IMG_URL):
            print(
                "[ERROR] - Your SOUNCLOUD_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if YOUTUBE_IMG_URL:
    if (
        YOUTUBE_IMG_URL
        != "https://64.media.tumblr.com/c39b07d55fbdff89661056be8bd08dbd/df2251522787e803-87/s1280x1920/40ae16b0ab0adadc2914146b115ab4ba0480863e.gifv"
    ):
        if not re.match("(?:http|https)://", YOUTUBE_IMG_URL):
            print(
                "[ERROR] - Your YOUTUBE_IMG_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()

if TELEGRAM_VIDEO_URL:
    if (
        TELEGRAM_VIDEO_URL
        != "https://64.media.tumblr.com/79bb5c54237323c17c93af4c3c83671b/667b875d0810726a-86/s1280x1920/018a7062497c7599991eac83a4f41844484e90e7.gifv"
    ):
        if not re.match("(?:http|https)://", TELEGRAM_VIDEO_URL):
            print(
                "[ERROR] - Your TELEGRAM_VIDEO_URL url is wrong. Please ensure that it starts with https://"
            )
            sys.exit()
