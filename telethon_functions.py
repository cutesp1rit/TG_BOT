from telethon import TelegramClient
from app.data_bot import api_id, api_hash, bot_token

client = TelegramClient('session_name', api_id, api_hash)

async def get_chat_members(chat_id):
    await client.start(bot_token=bot_token)
    chat_members = []
    async for member in client.iter_participants(chat_id):
        chat_members.append(member.username)
    await client.disconnect()
    return chat_members