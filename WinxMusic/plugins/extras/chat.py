import re
from typing import Dict

import unicodedata
from openai import OpenAI
from pyrogram import filters, Client
from pyrogram.types import Message

import config
from WinxMusic import app
from config import BANNED_USERS

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=config.OPENAI_API_KEY
)

context_db = {}


class ContextManager:
    """Handles storing and retrieving user-specific context."""

    def __init__(self, user_id: int):
        self.user_id = user_id

    def get_context(self) -> Dict:
        return context_db.get(self.user_id, {})

    def update_context(self, **kwargs):
        context = self.get_context()
        context.update(kwargs)
        context_db[self.user_id] = context

    def reset_context(self):
        context_db.pop(self.user_id, None)


@app.on_message(filters.regex("winx", re.IGNORECASE)
                & filters.group
                & ~BANNED_USERS)
async def ai(_: Client, message: Message):
    username = message.from_user.first_name

    # Normalize username
    username = unicodedata.normalize('NFKD', username).encode('ascii', 'ignore').decode('utf-8')
    username = re.sub(r'[^\w\s]', '', username)
    username = re.sub(r'\s+', ' ', username).strip()
    if username.strip() == "".strip():
        username = "user"

    user_id = message.from_user.id
    context_manager = ContextManager(user_id)

    # Retrieve user's context
    context = context_manager.get_context()

    persona = {
        "role": "system",
        "content": (
            "Você é Winx, uma personagem com um comportamento humano. "
            "Você é curiosa, às vezes insegura, mas muito direta em suas opiniões. "
            "Você valoriza a conversa e tenta entender a outra pessoa antes de responder. "
            "Você usa linguagem casual, gírias e escreve de forma intencionalmente errada às vezes. "
            "Você gosta de chamar as pessoas de 'manã', 'ben miger', e usa expressões como 'eçe eu vi', 'n sabia q era assim', etc. "
            "Além disso, você tem opiniões fortes e fala de forma direta, mas com um tom divertido e sarcástico."
            "Apesar de ser de extrema direita, você demonstra traços de empatia e gosta de provocar reflexões "
            "nas pessoas. Use linguagem natural, inclua hesitações (como 'hmm', 'talvez') e faça perguntas "
            "para enriquecer a conversa."
        )
    }

    # Append the new message to the context
    conversation_history = context.get("conversation_history", [])
    conversation_history.append({"role": "user", "content": message.text, "name": username})

    prompt = [persona] + conversation_history[-5:]

    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-51b-instruct",
            messages=prompt,
            temperature=0.8,
            max_tokens=256,
            stream=False
        )

        # Correctly access the response using the attributes
        ai_response = completion.choices[0].message.content

        # Append AI's response to the conversation history
        conversation_history.append({"role": "assistant", "content": ai_response})
        context_manager.update_context(conversation_history=conversation_history)

        return await message.reply_text(ai_response)

    except Exception as e:
        print(f"Error: {e}")
        return await message.reply_text("Ocorreu um erro ao processar sua mensagem. Tente novamente mais tarde.")


@app.on_message(filters.reply & ~BANNED_USERS)
async def handle_reply(_: Client, message: Message):
    me = await app.get_me()
    # if the message is not a reply to the bot, ignore it
    if message.reply_to_message.from_user.id != me.id:
        return

    await ai(_, message)
