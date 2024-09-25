import random

from WinxMusic import userbot
from WinxMusic.core.mongo import mongodb

db = mongodb.assistants

assistant_dict = {}


async def get_client(assistant: int) -> userbot:
    if int(assistant) == 1:
        return userbot.one
    elif int(assistant) == 2:
        return userbot.two
    elif int(assistant) == 3:
        return userbot.three
    elif int(assistant) == 4:
        return userbot.four
    elif int(assistant) == 5:
        return userbot.five


async def save_assistant(chat_id, number):
    number = int(number)
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": number}},
        upsert=True,
    )


async def set_assistant(chat_id) -> userbot:
    from WinxMusic.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistant_dict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    userbot = await get_client(ran_assistant)
    return userbot


async def get_assistant(chat_id: int) -> userbot:
    from WinxMusic.core.userbot import assistants

    assistant = assistant_dict.get(chat_id)
    if not assistant:
        dbassistant = await db.find_one({"chat_id": chat_id})
        if not dbassistant:
            userbot = await set_assistant(chat_id)
            return userbot
        else:
            got_assis = dbassistant["assistant"]
            if got_assis in assistants:
                assistant_dict[chat_id] = got_assis
                userbot = await get_client(got_assis)
                return userbot
            else:
                userbot = await set_assistant(chat_id)
                return userbot
    else:
        if assistant in assistants:
            userbot = await get_client(assistant)
            return userbot
        else:
            userbot = await set_assistant(chat_id)
            return userbot


async def set_calls_assistant(chat_id):
    from WinxMusic.core.userbot import assistants

    ran_assistant = random.choice(assistants)
    assistant_dict[chat_id] = ran_assistant
    await db.update_one(
        {"chat_id": chat_id},
        {"$set": {"assistant": ran_assistant}},
        upsert=True,
    )
    return ran_assistant


async def group_assistant(self, chat_id: int) -> userbot:
    from WinxMusic.core.userbot import assistants

    assistant = assistant_dict.get(chat_id)
    if not assistant:
        db_assistant = await db.find_one({"chat_id": chat_id})
        if not db_assistant:
            user_assistant = await set_calls_assistant(chat_id)
        else:
            user_assistant = db_assistant["assistant"]
            if user_assistant in assistants:
                assistant_dict[chat_id] = user_assistant
                user_assistant = user_assistant
            else:
                user_assistant = await set_calls_assistant(chat_id)
    else:
        if assistant in assistants:
            user_assistant = assistant
        else:
            user_assistant = await set_calls_assistant(chat_id)
    if int(user_assistant) == 1:
        return self.one
    elif int(user_assistant) == 2:
        return self.two
    elif int(user_assistant) == 3:
        return self.three
    elif int(user_assistant) == 4:
        return self.four
    elif int(user_assistant) == 5:
        return self.five
