# Configurações do Winx Music Bot

As variáveis de configuração (config vars) são basicamente as variáveis que configuram ou modificam o bot para funcionar, sendo as necessidades básicas para que plugins ou códigos operem. É necessário definir as variáveis obrigatórias para que o bot funcione e ative as funcionalidades básicas.

## Variáveis Obrigatórias

- Estas são as variáveis mínimas necessárias para configurar o Winx Music Bot para funcionar.

1. `API_ID`: Obtenha em my.telegram.org
2. `API_HASH`: Obtenha em my.telegram.org
3. `BOT_TOKEN`: Obtenha com o [@Botfather](http://t.me/BotFather) no Telegram
4. `MONGO_DB_URI`: Obtenha o URI do MongoDB em [MongoDB](https://cloud.mongodb.com)
5. `LOG_GROUP_ID`: Você precisará de um ID de Grupo Privado para isso. Supergrupo necessário com ID começando por -100
6. `OWNER_ID`: ID do proprietário para gerenciar o bot; IDs múltiplos podem ser separados por vírgulas.
7. `STRING_SESSIONS`: Strings de sessão Pyrogram v2 para múltiplos assistentes, separadas por vírgulas.

## Variáveis Não Obrigatórias

- Estas são variáveis extras para recursos adicionais no Music Bot. Você pode deixar as variáveis não obrigatórias por agora e adicioná-las depois.

1. `DURATION_LIMIT`: Duração máxima personalizada para áudio (música) no chat de voz. Padrão para 60 min.
2. `SONG_DOWNLOAD_DURATION_LIMIT`: Limite de duração para baixar músicas em formato MP3 ou MP4 pelo bot. Padrão para 180 min.
3. `VIDEO_STREAM_LIMIT`: Número máximo de chamadas de vídeo permitidas no bot. Pode ser ajustado posteriormente via /set_video_limit no Telegram. Padrão para 3 chats.
4. `SERVER_PLAYLIST_LIMIT`: Limite máximo para usuários salvarem playlists no servidor do bot. Padrão para 30.
5. `PLAYLIST_FETCH_LIMIT`: Limite máximo para buscar faixas da playlist de links do YouTube, Spotify, Apple. Padrão para 25.
6. `CLEANMODE_MINS`: Tempo após o qual o bot apagará suas mensagens antigas dos chats. Padrão para 5 min.
7. `SUPPORT_CHANNEL`: Se você tiver um canal para seu bot de música, insira o link do canal aqui.
8. `SUPPORT_GROUP`: Se você tiver um grupo de suporte para o bot, insira o link do grupo aqui.

## Limites de Tamanho de Arquivo para Reprodução

- Limite máximo de tamanho de arquivo para áudios e vídeos que podem ser reproduzidos pelo bot. [Apenas em bytes]

1. `TG_AUDIO_FILESIZE_LIMIT`: Tamanho máximo de arquivo para áudios transmitidos. Padrão para 104857600 bytes, ou 100MB.
2. `TG_VIDEO_FILESIZE_LIMIT`: Tamanho máximo de arquivo para vídeos reproduzidos. Padrão para 1073741824 bytes, ou 1GB.

## Variáveis do Bot

- Essas variáveis são usadas para configurar o bot. Você pode editá-las, se desejar, ou deixá-las como estão.

1. `PRIVATE_BOT_MODE`: Defina como `True` para tornar o bot privado ou `False` para todos os grupos. Padrão é `False`.
2. `YOUTUBE_EDIT_SLEEP`: Tempo de espera para o Downloader do YouTube. Padrão para 3 segundos.
3. `TELEGRAM_EDIT_SLEEP`: Tempo de espera para o Downloader do Telegram. Padrão para 5 segundos.
4. `AUTO_LEAVING_ASSISTANT`: Defina como `True` para que o assistente saia após um tempo determinado.
5. `ASSISTANT_LEAVE_TIME`: Tempo após o qual o assistente sairá dos chats automaticamente. Padrão para 5400 segundos, ou 90 min.
6. `SET_CMDS`: Defina como `True` para que o bot configure os comandos do menu de chat automaticamente.

## Variáveis do Spotify

- Para reproduzir músicas ou playlists do Spotify no Winx Music Bot. Essas variáveis não são essenciais, você pode deixá-las em branco.

1. `SPOTIFY_CLIENT_ID`: Obtenha em https://developer.spotify.com/dashboard
2. `SPOTIFY_CLIENT_SECRET`: Obtenha em https://developer.spotify.com/dashboard

## Variáveis do Heroku

- Necessário para usar comandos específicos do Heroku.

1. `HEROKU_API_KEY`: Obtenha em http://dashboard.heroku.com/account
2. `HEROKU_APP_NAME`: Nome do app no Heroku para identificar seu Music Bot.

## Variáveis de Repositório Personalizado

- Para usar o Winx Music Bot com seu próprio código personalizado.

1. `UPSTREAM_REPO`: URL do seu repositório.
2. `UPSTREAM_BRANCH`: Branch padrão do seu repositório.
3. `GIT_TOKEN`: Seu token do Git caso o repositório seja privado.
4. `GITHUB_REPO`: URL do seu repositório GitHub que será exibido no comando /start.

## Variáveis de Imagem/Thumbnail

- Você pode alterar as imagens usadas no Winx Music Bot.

1. `START_IMG_URL`: Imagem para o comando /start em mensagens privadas.
2. `PING_IMG_URL`: Imagem para o comando /ping do bot.
3. `PLAYLIST_IMG_URL`: Imagem para o comando /play.
4. `GLOBAL_IMG_URL`: Imagem para o comando /stats.
5. `STATS_IMG_URL`: Imagem para o comando /stats.
6. `TELEGRAM_AUDIO_URL`: Imagem para áudios do Telegram.
7. `TELEGRAM_VIDEO_URL`: Imagem para vídeos do Telegram.
8. `STREAM_IMG_URL`: Imagem para transmissões m3u8 ou links index.
9. `SOUNDCLOUD_IMG_URL`: Imagem para músicas do SoundCloud.
10. `YOUTUBE_IMG_URL`: Imagem caso o gerador de thumbnail falhe.
11. `SPOTIFY_ARTIST_IMG_URL`: Imagem para artistas do Spotify.
12. `SPOTIFY_ALBUM_IMG_URL`: Imagem para álbuns do Spotify.
13. `SPOTIFY_PLAYLIST_IMG_URL`: Imagem para playlists do Spotify.

## Modo Multi Assistente

- Suporta clientes de assistente ilimitados.

`STRING_SESSIONS`: Adicione múltiplas strings de sessão Pyrogram v2, separadas por vírgulas.
