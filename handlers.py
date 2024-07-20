from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.pyrogram_functions import get_chat_members
from app.data_bot import bot_token

bot = Bot(token=bot_token)
router = Router()
dict_chats = dict()

async def check_data(message: Message):
    id = message.chat.id
    if (type(dict_chats.get(id, -1)) is int):
        dict_chats[id] = list()
        chat_members = await get_chat_members(id)
        print(chat_members)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await check_data(message)
    await message.answer_sticker("CAACAgIAAxkBAAEMgrhmmSOEjUk0snQE3IgDG0z0evKZQgACZCAAAttj0UhGGc1kRg_sVTUE")
    if message.from_user.id == 894566791:
        await message.reply("привет зая")
    elif message.from_user.id == 634734136:
        await message.reply("ЗАТКНИСЬ ДУРААААА")

@router.message(Command('new_list'))
async def cmd_new_list(message: Message):
    await check_data(message)

@router.message(Command('remove_list'))
async def cmd_remove_list(message: Message):
    await check_data(message)

@router.message()
async def universal(message: Message):
    await check_data(message)