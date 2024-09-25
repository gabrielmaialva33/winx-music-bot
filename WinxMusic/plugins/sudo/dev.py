import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from WinxMusic.utils.cleanmode import protect_message


async def aexec(code: str, client: Client, message: Message):
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


async def edit_or_reply(msg: Message, **kwargs: dict):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})
    await protect_message(msg.chat.id, msg.id)


@app.on_edited_message(
    filters.command(["ev", "eval"]) & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
@app.on_message(
    filters.command(["ev", "eval"]) & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
async def executor(client: Client, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>O que você quer executar, querido?</b>")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await message.delete()
    t1 = time()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = "\n"
    if exc:
        evaluation += exc
    elif stderr:
        evaluation += stderr
    elif stdout:
        evaluation += stdout
    else:
        evaluation += "Success"
    final_output = f"<b>⥤ Resultado:</b>\n<pre language='python'>{evaluation}</pre>"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation))
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {t2 - t1} Seconds",
                    )
                ]
            ]
        )
        await message.reply_document(
            document=filename,
            caption=f"<b>⥤ Avaliação:</b>\n<code>{cmd[0:980]}</code>\n\n<b>⥤ Resultado:</b>\nDocumento anexado",
            quote=False,
            reply_markup=keyboard,
        )
        await message.delete()
        os.remove(filename)
    else:
        t2 = time()
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⏳",
                        callback_data=f"runtime {round(t2 - t1, 3)} Seconds",
                    ),
                    InlineKeyboardButton(
                        text="🗑",
                        callback_data=f"forceclose abc|{message.from_user.id}",
                    ),
                ]
            ]
        )
        await edit_or_reply(message, text=final_output, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"runtime"))
async def runtime_func_cq(_, cq):
    runtime = cq.data.split(None, 1)[1]
    await cq.answer(runtime, show_alert=True)


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(
                "» Será melhor se você ficar nos seus limites, querido.", show_alert=True
            )
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return


@app.on_edited_message(
    filters.command("sh") & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
@app.on_message(filters.command("sh") & SUDOERS & ~filters.forwarded & ~filters.via_bot)
async def shellrunner(_, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>Exemplo :</b>\n/sh git pull")
    text = message.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                await edit_or_reply(message, text=f"<b>ERRO :</b>\n<pre>{err}</pre>")
            output += f"<b>{code}</b>\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await edit_or_reply(
                message, text=f"<b>ERRO :</b>\n<pre>{''.join(errors)}</pre>"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.id,
                caption="<code>Saída</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>SAÍDA :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>SAÍDA :</b>\n<code>Nenhum</code>")

    await message.stop_propagation()


__MODULE__ = "Dev"
__HELP__ = """
🔰<b><u>Adicionar e Remover Usuários Sudo:</u></b>

★ <b>/addsudo [Nome de usuário ou Responder a um usuário]</b>
★ <b>/delsudo [Nome de usuário ou Responder a um usuário]</b>

🛃<b><u>Heroku:</u></b>

★ <b>/usage</b> - Uso de Dyno.
★ <b>/get_var</b> - Obter uma variável de configuração do Heroku ou .env
★ <b>/del_var</b> - Deletar qualquer variável no Heroku ou .env.
★ <b>/set_var [Nome da Variável] [Valor]</b> - Definir ou atualizar uma variável no Heroku ou .env. Separe o nome da variável e seu valor com um espaço.

🤖<b><u>Comandos do Bot:</u></b>

★ <b>/restart</b> - Reiniciar seu Bot.
★ <b>/update , /gitpull</b> - Atualizar o Bot.
★ <b>/speedtest</b> - Verificar a velocidade do servidor
★ <b>/maintenance [habilitar / desabilitar]</b>
★ <b>/logger [habilitar / desabilitar]</b> - O Bot registra as consultas pesquisadas no grupo de registro.
★ <b>/get_log [Número de Linhas]</b> - Obter o log do seu bot do Heroku ou VPS. Funciona para ambos.
★ <b>/autoend [habilitar|desabilitar]</b> - Habilitar encerramento automático da reprodução após 3 minutos se ninguém estiver ouvindo.
"""
