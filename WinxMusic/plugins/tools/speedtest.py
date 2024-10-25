import asyncio

from pyrogram import filters

import speedtest
from WinxMusic import app
from WinxMusic.misc import SUDOERS
from strings import get_command

SPEEDTEST_COMMAND = get_command("SPEEDTEST_COMMAND")


def testspeed(m):
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = m.edit("⇆ Testando **download** ... ⬇️")
        test.download()
        m = m.edit("⇆ Testando **upload** ... ⬆️")
        test.upload()
        test.results.share()
        result = test.results.dict()
        m = m.edit("↻ Compartilhando os resultados do SpeedTest ... 📊")
    except Exception as e:
        return m.edit(f"⚠️ Erro: {e}")
    return result


@app.on_message(filters.command(SPEEDTEST_COMMAND) & SUDOERS)
async def speedtest_function(client, message):
    m = await message.reply_text("🚀 **Iniciando SpeedTest**...")
    loop = asyncio.get_event_loop_policy().get_event_loop()
    result = await loop.run_in_executor(None, testspeed, m)
    output = f"""**Resultados do SpeedTest** 📊

<u>**Cliente:**</u>
🌐 **ISP :** {result['client']['isp']}
🏳️ **País :** {result['client']['country']}

<u>**Servidor:**</u>
🌍 **Nome :** {result['server']['name']}
🇦🇺 **País:** {result['server']['country']}, {result['server']['cc']}
💼 **Patrocinador:** {result['server']['sponsor']}
⚡ **Latência:** {result['server']['latency']} ms  
🏓 **Ping :** {result['ping']} ms"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=result["share"], caption=output
    )
    await m.delete()
