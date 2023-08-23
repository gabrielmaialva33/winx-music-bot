<h1 align="center">
  <br>
  <img src="https://64.media.tumblr.com/b20a9df719f8420ac7aa02ece2cb1774/5f8ef1a042cf9e6b-7f/s540x810/eba21bbdb525e72f84be27d439c156b4dfa6b31a.gifv" alt="Winx Bot" width="400">
  <br>
  Winx Bot for <a href="https://telegram.org/">Telegram</a>
  <br>
</h1>

<p align="center">
  <img src="https://wakatime.com/badge/user/e61842d0-c588-4586-96a3-f0448a434be4/project/606f5c48-9148-446c-b6f7-d12aafbaaee8.svg" alt="wakatime">
  <img src="https://img.shields.io/github/languages/top/gabrielmaialva33/winx-music-bot?style=flat&logo=appveyor" alt="GitHub top language" >
  <img src="https://img.shields.io/github/languages/count/gabrielmaialva33/winx-music-bot?style=flat&logo=appveyor" alt="GitHub language count" >
  <img src="https://img.shields.io/github/repo-size/gabrielmaialva33/winx-music-bot?style=flat&logo=appveyor" alt="Repository size" >
  <img src="https://img.shields.io/github/license/gabrielmaialva33/winx-music-bot?color=00b8d3?style=flat&logo=appveyor" alt="License" /> 
  <a href="https://github.com/gabrielmaialva33/winx-music-bot/commits/master">
    <img src="https://img.shields.io/github/last-commit/gabrielmaialva33/winx-music-bot?style=flat&logo=appveyor" alt="GitHub last commit" >
    <img src="https://img.shields.io/badge/made%20by-Maia-15c3d6?style=flat&logo=appveyor" alt="Maia" >  
  </a>
</p>

<p align="center">
  <a href="#bookmark-about">About</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#computer-technologies">Technologies</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#package-installation">Installation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#wrench-configuration">Configuration</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-documentation">Documentation</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#memo-license">License</a>
</p>

<br>

## :bookmark: About

**Winx Bot** é um bot de música e vídeo para o Telegram escrito em Python, utilizando Phoenix, através do qual você pode
transmitir músicas, vídeos e até mesmo transmissões ao vivo nas suas chamadas em grupo por meio de várias fontes. 🎵🎥✨

* YouTube, Soundcloud, Apple Music, Spotify, Resso, Live Streams and Telegram Audios & Videos support.
* Written from scratch, making it stable and less crashes with attractive thumbnails.
* Loop, Seek, Shuffle, Specific Skip, Playlists etc support
* Multi-Language support

<br>

## :computer: Technologies

- **[Python](https://www.python.org/)**
- **[PyTgCalls](https://github.com/pytgcalls/pytgcalls)**
- **[Pyrogram](https://docs.pyrogram.org/)**
- **[MongoDB](https://www.mongodb.com/)**
- **[FFmpeg](https://ffmpeg.org/)**
- **[Pillow](https://pillow.readthedocs.io/en/stable/)**

## :package: Installation

```bash
# install ffmpeg
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y --no-install-recommends ffmpeg
# clone the repository
git clone https://github.com/gabrielmaialva33/winx-music-bot.git
# enter the directory
cd winx-music-bot
# install the dependencies
pip3 install --no-cache-dir --upgrade --requirement requirements.txt
```

### :wrench: **Configuration**

copy the sample.env file to .env and fill the values

```bash
# Configure .env file
cp sample.env .env
# generate session string
python3 genstring.py
# run the bot
python3 -m WinxMusic
```

### :memo: **Documentation**

```md
# coming soon
```

### :writing_hand: **Author**

| [![Maia](https://avatars.githubusercontent.com/u/26732067?size=100)](https://github.com/gabrielmaialva33) |
|-----------------------------------------------------------------------------------------------------------|
| [Maia](https://github.com/gabrielmaialva33)                                                               |

## License

[MIT License](./LICENSE)
