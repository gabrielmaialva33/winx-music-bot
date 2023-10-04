HELP_1 = """🎉**<u>Comandos para Administradores</u>**🎉

- **c** para tocar música no canal.
- **v** para tocar música por voz.
- **force** para tocar música imediatamente.

🎵**<u>Controles de Música</u>**🎵

- /pause ou /cpause: Pausar a música.
- /resume ou /cresume: Retomar a música.
- /mute ou /cmute: Silenciar a música.
- /unmute ou /cunmute: Tirar o silêncio da música.
- /skip ou /cskip: Avançar a música.
- /stop ou /cstop: Parar a música.
- /shuffle ou /cshuffle: Embaralhar a playlist.
- /seek ou /cseek: Ir para um momento específico da música.
- /seekback ou /cseekback: Voltar para um momento específico da música.
- /restart: Reiniciar o bot.

🔄**<u>Modo Loop</u>**🔄

- /loop ou /cloop [ativar/desativar] ou [um número entre 1-10]: Repete a música atual de 1 a 10 vezes. Padrão é 10 vezes.

👥**<u>Usuários Autorizados</u>**👥

Usuários autorizados podem usar comandos administrativos mesmo sem serem administradores no chat.

- /auth [Nome de usuário]: Adicionar um usuário à lista de autorizados.
- /unauth [Nome de usuário]: Remover um usuário da lista de autorizados.
- /authusers: Ver a lista de usuários autorizados.
"""

HELP_2 = """🎬<u>**Reprodução de Música/Vídeo:**</u>🎬

Comandos disponíveis: play, vplay, cplay
Comandos de força: playforce, vplayforce, cplayforce

- **c**: para reprodução no canal.
- **v**: para reprodução por voz.
- **force**: para reprodução imediata.

- /play, /vplay ou /cplay: O bot começa a tocar sua pesquisa no chat de voz ou transmite links ao vivo.

- /playforce, /vplayforce ou /cplayforce: O bot começa a tocar sua pesquisa. Se já estiver tocando algo, para e toca a nova música.

- /channelplay [Nome de usuário do chat ou id] ou [Desativar]: Toca música em um canal específico. Exemplo: /channelplay @WinxMusicBot ou /channelplay -1001234567890

📜<u>**Playlist**</u>📜

- /playlist: Mostra todas as playlists disponíveis no servidor.
- /deleteplaylist: Deleta uma playlist do servidor.
- /play: Toca uma playlist do servidor.
"""

HELP_3 = """✅<u>**Comandos do Bot**</u>✅

/stats - Exibe estatísticas do bot.

/sudolist - Lista usuários sudo.

/lyrics [Nome da Música] - Exibe letra da música.

/song [Nome da Faixa] ou [Link do YT] - Baixa a música.

/player - Exibe configurações do player.

**c** - Para reprodução no canal.

/queue ou /cqueue - Exibe fila de reprodução."""

HELP_4 = """✅<u>**Comandos Extras**</u>✅
/start - Inicia o bot.
/help - Lista todos os comandos.
/ping - Exibe o ping do bot.

✅<u>**Configurações do Grupo**</u>✅
/settings - Exibe as configurações do grupo.

🔗 **Opções de Configuração:**

1️⃣ **Qualidade de Áudio:** Defina a qualidade do áudio para transmitir no chat de voz.

2️⃣ **Qualidade de Vídeo:** Defina a qualidade do vídeo para transmitir no chat de voz.

3️⃣ **Usuários Autorizados:** Altere o acesso aos comandos administrativos para todos ou apenas administradores. Se definido para todos, qualquer um no grupo pode usar comandos de administração, como /skip, /stop, etc.

4️⃣ **Modo Limpo:** Se ativado, o bot apagará todas as mensagens de comando após 5 minutos.

5️⃣ **Limpeza de Comandos:** Se ativado, o bot apagará todos os comandos (/play, /pause, /shuffle, /stop, etc.) imediatamente após serem executados.

6️⃣ **Configurações de Reprodução:**

/playmode - Altere o modo de reprodução do bot aqui.

<u>Opções de Modo de Reprodução:</u>

1️⃣ **Modo de Busca** [Direto ou Inline] - Se definido como direto, o bot reproduzirá a música diretamente. Se definido como inline, o bot enviará uma mensagem inline com a música a ser reproduzida.

2️⃣ **Comandos de Admin** [Todos ou Admins] - Defina se todos no grupo ou apenas administradores podem usar comandos de administração, como /skip, /stop, etc.

3️⃣ **Tipo de Reprodução** [Todos ou Admins] - Defina se todos no grupo ou apenas administradores podem usar comandos de reprodução, como /play, /pause, etc."""

HELP_5 = """🔰<u>**ADD & REMOVE SUDO USERS:**</u>
/addsudo [Nome de usuário ou Resposta a um usuário] - Adiciona um usuário sudo.
/delsudo [Nome de usuário ou Resposta a um usuário] - Remove um usuário sudo.

🛃<u>**HEROKU:**</u>
/usage - Uso do Dyno.
/get_var - Exibe todas as variáveis de configuração do Heroku.
/del_var - Apaga uma variável de configuração do Heroku.
/set_var [Nome da Variável] [Valor] - Define uma variável de configuração do Heroku.

🤖<u>**COMANDOS DO BOT:**</u>
/reboot - Reinicia o bot.
/update - Atualiza o bot.
/speedtest - Teste de velocidade do servidor.
/maintenance [enable/disable] - Ativa/Desativa o modo de manutenção.
/logger [enable/disable] - Ativa/Desativa o modo de log.
/get_log [Número de Linhas] - Obtém o log do bot.
/autoend [enable|disable] - Ativa/Desativa a saída automática do bot do chat de voz após 3 minutos sem usuários.

📈<u>**COMANDOS DE ESTATÍSTICAS:**</u>
/activevoice - Exibe todos os chats de voz ativos.
/activevideo - Exibe todos os chats de vídeo ativos.
/stats - Exibe as estatísticas do bot.

⚠️<u>**FUNÇÃO DE BLACKLIST DE CHAT:**</u>
/blacklistchat [CHAT_ID] - Adiciona um chat à blacklist.
/whitelistchat [CHAT_ID] - Remove um chat da blacklist.
/blacklistedchat - Exibe todos os chats na blacklist.

👤<u>**FUNÇÃO DE BLOQUEIO:**</u>
/block [Nome de usuário ou Resposta a um usuário] - Bloqueia um usuário.
/unblock [Nome de usuário ou Resposta a um usuário] - Desbloqueia um usuário.
/blockedusers - Exibe todos os usuários bloqueados.

👤<u>**FUNÇÃO GBAN:**</u>
/gban [Nome de usuário ou Resposta a um usuário] - Bane globalmente um usuário.
/ungban [Nome de usuário ou Resposta a um usuário] - Desbane globalmente um usuário.
/gbannedusers - Exibe todos os usuários banidos globalmente.

🎥<u>**FUNÇÃO DE CHAMADAS DE VÍDEO:**</u>
/set_video_limit [Número de Chats] - Define o limite de chats de vídeo. (Padrão: 3)
/videomode [download|m3u8] - Se o modo baixar estiver ativado, o bot baixará os vídeos em vez de reproduzi-los no formato M3u8. O padrão é M3u8. Use o modo baixar se uma consulta não for reproduzida no modo m3u8.

⚡️<u>**FUNÇÃO DE BOT PRIVADO:**</u>
/authorize [CHAT_ID] - Autoriza um chat a usar o bot.
/unauthorize [CHAT_ID] - Desautoriza um chat a usar o bot.
/authorized - Exibe todos os chats autorizados a usar o bot.

🌐<u>**FUNÇÃO DE TRANSMISSÃO:**</u>
/broadcast [Mensagem ou Resposta a uma Mensagem] - Envia uma mensagem para todos os chats autorizados.

<u>Opções de Transmissão:</u>

**-pin** : Fixa a mensagem enviada.
**-pinloud** : Fixa a mensagem enviada e envia um alerta.
**-user** : Envia a mensagem para todos os usuários autorizados.
**-assistant** : Envia a mensagem para todos os usuários autorizados e o assistente.
**-nobot** : Envia a mensagem para todos os usuários autorizados, exceto o bot.

**Exemplo:** `/broadcast -user -assistant -pin Boa tarde!`"""
