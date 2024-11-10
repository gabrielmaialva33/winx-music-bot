import asyncio

from pyrogram import Client as c


async def generate_session(api_id, api_hash):
    i = c("winxstring", in_memory=True, api_id=api_id, api_hash=api_hash)

    await i.start()
    ss = await i.export_session_string()
    session_message = (
        "HERE IS YOUR STRING SESSION, COPY IT, DON'T SHARE!!\n\n"
        f"`{ss}`\n\nSTRING GENERATED SUCCESSFULLY!"
    )
    try:
        await i.send_message("me", session_message)
        print("Session string sent to your saved messages!")
    except BaseException:
        pass

    print(session_message)
    return ss


def start_session_generation():
    api_id = input("\nEnter Your API ID:\n> ")
    api_hash = input("\nEnter Your API HASH:\n> ")

    if not api_id or not api_hash:
        print("Please enter both API ID and API HASH!")
        return

    try:
        int(api_id)
    except ValueError:
        print("API ID must be a number!")
        return

    asyncio.run(generate_session(api_id, api_hash))


if __name__ == "__main__":
    print("Welcome to Pyrogram String Session Generator!")
    start_session_generation()
