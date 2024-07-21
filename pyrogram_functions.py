from pyrogram import Client
from app.data_bot import api_hash, api_id, bot_token


async def get_chat_members(chat_id):
    app = Client("Bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members = []
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members = chat_members + [member.user.username]
    await app.stop()
    return chat_members