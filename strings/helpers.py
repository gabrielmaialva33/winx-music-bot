#
# Copyright (C) 2021-2023 by Maia, < https://github.com/gabrielmaialva33 >.
#
# This file is part of < https://github.com/gabrielmaialva33/winx-music-bot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/gabrielmaialva33/winx-music-bot/blob/master/LICENSE >
#
# All rights reserved.

HELP_1 = """✅**<u>Admin Comandos</u>**✅

**c** para reprodução de canal.
**v** para reprodução de voz.
**force** para reprodução forçada.

/pause or /cpause - Pause a música.
/resume or /cresume- Continuar a música.
/mute or /cmute- Mute a música.
/unmute or /cunmute- Desmute a música.
/skip or /cskip- Pular a música.
/stop or /cstop- Parar a música.
/shuffle or /cshuffle- Embaralhar a fila.
/seek or /cseek - Pular para um tempo específico da música.
/seekback or /cseekback - Voltar para um tempo específico da música.
/restart - Reiniciar o bot.


✅<u>**Comandos de Música**</u>✅
/skip or /cskip [Número(example: 3)] 
    - Pula a música para um número especificado na fila. Exemplo: /skip 3 ou /cskip 3 para pular para a terceira música na fila.

✅<u>**Em loop:**</u>
/loop or /cloop [enable/disable] ou [Um número entre 1-10] 
    - Quando ativado, o bot repete a reprodução da música atual de 1 a 10 vezes no bate-papo por voz. Padrão para 10 vezes.

✅<u>**Usuários Autorizados:**</u>
Usuários Autorizados podem usar comandos administrativos sem direitos administrativos em seu chat.

/auth [Username] - Adicionar um usuário à lista de usuários autorizados.
/unauth [Username] - Remover um usuário da lista de usuários autorizados.
/authusers - Lista de usuários autorizados."""

HELP_2 = """✅<u>**Reprodução de Música/Vídeo:**</u>

Comandos Disponíveis = play , vplay , cplay

Comandos Forçar = playforce , vplayforce , cplayforce

**c** para reprodução de canal.
**v** para reprodução de voz.
**force** para reprodução forçada.

/play or /vplay or /cplay  - O bot começará a reproduzir sua consulta no chat de voz ou transmitir links ao vivo em seu chat de voz.

/playforce or /vplayforce or /cplayforce -  O bot começará a reproduzir sua consulta no chat de voz ou transmitir links ao vivo em seu chat de voz. Se o bot estiver reproduzindo algo, ele será parado e a nova música será reproduzida.

/channelplay [Chat username or id] or [Disable] - Reproduzir música em um canal específico. Exemplo: /channelplay @WinxMusicBot ou /channelplay -1001234567890


✅**<u>Playlist</u>**✅
/playlist  - Mostra todas as playlists disponíveis no servidor.
/deleteplaylist - Deletar uma playlist do servidor.
/play  - Reproduzir uma playlist do servidor."""

HELP_3 = """✅<u>**Bot Comandos**</u>✅

/stats - Mostra as estatísticas do bot.

/sudolist - Mostra todos os usuários sudo.

/lyrics [Music Name] - Mostra a letra da música.

/song [Track Name] or [YT Link] - Baixar música.

/player -  Mostra as configurações do player.

**c** para reprodução de canal.

/queue or /cqueue- Mostra a fila de reprodução."""

HELP_4 = """✅<u>**Comandos Extras**</u>✅
/start - Iniciar o bot.
/help  - Mostra todos os comandos disponíveis.
/ping  - Mostra o ping do bot.

✅<u>**Cofiurações do Grupo**</u>✅
/settings - Mostra as configurações do grupo.

🔗 **Opções em Configurações:**

1️⃣ Você pode definir a **Qualidade de áudio** que deseja transmitir no chat de voz.

2️⃣ Você pode definir a **Qualidade de video** que deseja transmitir no chat de voz.

3️⃣ **Auth Users**:- Você pode alterar o modo de comandos administrativos daqui para todos ou somente administradores. Se todos, qualquer pessoa presente em seu grupo poderá usar comandos de administração (como /skip, /stop etc)

4️⃣ **Clean Mode:** Quando ativado, o bot limpará todas as mensagens de comando do bot após 5 minutos.

5️⃣ **Command Clean** : Quando ativado, o bot limpará todos (/play, /pause, /shuffle, /stop etc) imediatamente após o comando ser executado.

6️⃣ **Play Settings:**

/playmode - Você pode alterar o modo de reprodução do bot aqui.

<u>Opções de tipo de reprodução:</u>

1️⃣ **Search Mode** [Direct or Inline] - Quando definido como direto, o bot irá reproduzir a música diretamente. Quando definido como inline, o bot irá enviar uma mensagem inline com a música que você deseja reproduzir.

2️⃣ **Admin Commands** [Everyone or Admins] - Quando definido como todos, qualquer pessoa presente em seu grupo poderá usar comandos de administração (como /skip, /stop etc). Quando definido como administradores, apenas administradores poderão usar comandos de administração.

3️⃣ **Play Type** [Everyone or Admins] - Quando definido como todos, qualquer pessoa presente em seu grupo poderá usar comandos de reprodução (como /play, /pause etc). Quando definido como administradores, apenas administradores poderão usar comandos de reprodução."""

HELP_5 = """🔰**<u>ADD & REMOVE SUDO USERS :</u>**
/addsudo [Username or Reply to a user] - Adicionar um usuário sudo.
/delsudo [Username or Reply to a user] - Remover um usuário sudo.

🛃**<u>HEROKU:</u>**
/usage - Dyno Usage.

🌐**<u>CONFIG VARS:</u>**
/get_var - Mostra todas as variáveis de configuração do Heroku.
/del_var - Deletar uma variável de configuração do Heroku.
/set_var [Var Name] [Value] - Definir uma variável de configuração do Heroku.

🤖**<u>BOT COMMANDS:</u>**
/reboot - Reiniciar o bot.
/update - Atualizar o bot.
/speedtest - Teste de velocidade do servidor.
/maintenance [enable / disable] - Ativar / desativar o modo de manutenção.
/logger [enable / disable] - Ativar / desativar o modo de log.
/get_log [Number of Lines] - Obter o log do bot.
/autoend [enable|disable] - Ativar / desativar a saida automática do bot quando não houver usuários no chat de voz. Apos 3 minutos o bot sai do chat de voz.

📈**<u>STATS COMMANDS:</u>**
/activevoice - Mostra todos os chats de voz ativos.
/activevideo - Mostra todos os chats de vídeo ativos.
/stats - Mostra as estatísticas do bot.

⚠️**<u>BLACKLIST CHAT FUNCTION:</u>**
/blacklistchat [CHAT_ID] - Adicionar um chat à lista negra.
/whitelistchat [CHAT_ID] - Remover um chat da lista negra.
/blacklistedchat - Mostrar todos os chats na lista negra.

👤**<u>BLOCKED FUNCTION:</u>**
/block [Username or Reply to a user] - Bloquear um usuário.
/unblock [Username or Reply to a user] - Desbloquear um usuário.
/blockedusers - Mostrar todos os usuários bloqueados.

👤**<u>GBAN FUNCTION:</u>**
/gban [Username or Reply to a user] - Banir globalmente um usuário.
/ungban [Username or Reply to a user] - Desbanir globalmente um usuário.
/gbannedusers - Mostrar todos os usuários banidos globalmente.

🎥**<u>VIDEOCALLS FUNCTION:</u>**
/set_video_limit [Number of Chats] - Definir o limite de chats de vídeo. (Padrão: 3)
/videomode [download|m3u8] - Se o modo de download estiver ativado, o Bot baixará os vídeos em vez de reproduzi-los no formato M3u8. Por padrão para M3u8. Você pode usar o modo de download quando qualquer consulta não for reproduzida no modo m3u8.

⚡️**<u>PRIVATE BOT FUNCTION:</u>**
/authorize [CHAT_ID] - Autorizar um chat para usar o bot.
/unauthorize [CHAT_ID] - Desautorizar um chat para usar o bot.
/authorized - Mostrar todos os chats autorizados para usar o bot.

🌐**<u>BROADCAST FUNCTION:</u>**
/broadcast [Message or Reply to a Message] - Enviar uma mensagem para todos os chats autorizados.

<u>opcões de broadcast:</u>

**-pin** : Fixar a mensagem enviada.
**-pinloud** : Fixar a mensagem enviada e enviar uma mensagem de alerta.
**-user** : Enviar a mensagem para todos os usuários autorizados.
**-assistant** : Enviar a mensagem para todos os usuários autorizados e o assistente.
**-nobot** : Enviar a mensagem para todos os usuários autorizados, exceto o bot.

**Exemplo:** `/broadcast -user -assistant -pin Boe die!`

"""
