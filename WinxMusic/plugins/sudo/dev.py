import os
import re
import subprocess
import sys
import traceback
from inspect import getfullargspec
from io import StringIO
from time import time

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from WinxMusic import app
from WinxMusic.misc import SUDOERS
from strings import get_command


async def aexec(code, client, message):
    local_vars = {}
    exec(
        "async def __aexec(client, message): "
        + "".join(f"\n {a}" for a in code.split("\n")),
        globals(),
        local_vars,
    )
    __aexec_func = local_vars["__aexec"]
    return await __aexec_func(client, message)


async def edit_or_reply(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


@app.on_edited_message(
    filters.command(["ev", "eval"]) & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
@app.on_message(
    filters.command(["ev", "eval"]) & SUDOERS & ~filters.forwarded & ~filters.via_bot
)
async def executor(client: app, message: Message):
    if len(message.command) < 2:
        return await edit_or_reply(message, text="<b>Give me something to exceute</b>")
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
    final_output = f"<b>RESULTS:</b>\n<pre language='python'>{evaluation}</pre>"
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
            caption=f"<b>EVAL :</b>\n<code>{cmd[0:980]}</code>\n\n<b>Results:</b>\nAttached Document",
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
                "This is not for you stay away from here", show_alert=True
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
        return await edit_or_reply(
            message, text="<b>Give some commamds like:</b>\n/sh git pull"
        )
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
                await edit_or_reply(message, text=f"<b>ERROR :</b>\n<pre>{err}</pre>")
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
                message, text=f"<b>ERROR :</b>\n<pre>{''.join(errors)}</pre>"
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
                caption="<code>Output</code>",
            )
            return os.remove("output.txt")
        await edit_or_reply(message, text=f"<b>OUTPUT :</b>\n<pre>{output}</pre>")
    else:
        await edit_or_reply(message, text="<b>OUTPUT :</b>\n<code>None</code>")

    await message.stop_propagation()


def command(cmd: str):
    cmds = " ".join([f"/{c}" for c in get_command(cmd)])
    return cmds


__MODULE__ = "Dev"
__HELP__ = f"""
<b><u>Adicionar e remover sudoers:</u></b>

<b>{command("ADDSUDO_COMMAND")} [Nome de usuário ou responder a um usuário] - Adicionar sudo ao seu bot</b>
<b>{command("DELSUDO_COMMAND")} [Nome de usuário, ID do usuário ou responder a um usuário] - Remover dos sudoers do bot</b>
<b>{command("SUDOUSERS_COMMAND")} - Obter uma lista de todos os sudoers</b>

<b><u>Comandos do Bot:</u></b>

<b>{command("RESTART_COMMAND")}</b> - Reiniciar o bot (apenas SUDOERS)
<b>{command("UPDATE_COMMAND")}</b> - Atualizar o bot
<b>{command("SPEEDTEST_COMMAND")}</b> - Verificar a velocidade do servidor
<b>{command("MAINTENANCE_COMMAND")} [ativar / desativar]</b> - Ativar ou desativar o modo de manutenção do bot
<b>{command("LOGGER_COMMAND")} [ativar / desativar]</b> - Ativar ou desativar o registro de consultas pesquisadas no grupo de logs
<b>{command("GETLOG_COMMAND")} [Número de linhas]</b> - Obter logs do servidor
<b>{command("AUTOEND_COMMAND")} [ativar / desativar]</b> - Encerrar automaticamente a transmissão após 30 segundos se ninguém estiver ouvindo músicas
"""
