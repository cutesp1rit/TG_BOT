from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.pyrogram_functions import get_chat_members
from app.data_bot import bot_token
from user import User

bot = Bot(token=bot_token)
router = Router()
dict_chats = dict()

async def check_data(message: Message):
    id = message.chat.id
    if (type(dict_chats.get(id, -1)) is int):
        dict_chats[id] = list()
        chat_members = await get_chat_members(id)
        # убираем бота из списка пользователей
        chat_without_bot = [member for member in chat_members if member != "produc1_manager_bot"]
        dict_chats[id] = [User(member, chat_without_bot) for member in chat_without_bot]


@router.message(CommandStart())
async def cmd_start(message: Message):
    await check_data(message)
    await message.reply("привет, сейчас я расскажу, как работает бот...")

@router.message(Command('download_cheque'))
async def cmd_new_list(message: Message):
    await check_data(message)
    

@router.message(Command('new_list'))
async def cmd_new_list(message: Message):
    await check_data(message)

@router.message(Command('remove_list'))
async def cmd_remove_list(message: Message):
    await check_data(message)

@router.message()
async def universal(message: Message):
    await check_data(message)