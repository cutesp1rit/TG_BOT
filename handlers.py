from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.pyrogram_functions import get_chat_members
from app.data_bot import bot_token
from app.user import User
from app.chat import Chat
from app.states import DownloadCheque
from aiogram.fsm.context import FSMContext
import app.keyboards as kb
import pandas as pd


# переименовать методы

bot = Bot(token=bot_token)
router = Router()
dict_chats = dict()

async def make_cheque(message: Message):
    products = DownloadCheque.products
    for i in products.items():
        await message.answer(f'Сколько человек будут скидываться на продукт "{i}"?')


async def check_data(message: Message):
    id = message.chat.id
    if (type(dict_chats.get(id, -1)) is int):
        dict_tmp = dict()
        chat_members = await get_chat_members(id)
        # убираем бота из списка пользователей
        chat_without_bot = [member for member in chat_members if member != "produc1_manager_bot"]
        for member in chat_without_bot:
            dict_tmp[member] = User(member, chat_without_bot)
        dict_chats[id] = Chat(dict_tmp)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await check_data(message)
    await message.answer("Привет, сейчас я расскажу, как работает бот...")


@router.message(Command('download_cheque'))
async def cmd_download_cheque(message: Message, state: FSMContext):
    # await check_data(message)
    await message.reply("Напишите количество позиций, которое будет в чеке:")
    await state.set_state(DownloadCheque.count_of_positions)

@router.message(DownloadCheque.count_of_positions)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat = dict_chats[message.chat.id]
    try:
        await state.update_data(count_of_positions=int(message.text))
        curr_chat.count_pos = int(message.text)
        await state.set_state(DownloadCheque.product)
        await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main + 1}:")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

@router.message(DownloadCheque.product)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat = dict_chats[message.chat.id]
    await state.update_data(product=message.text)
    await state.set_state(DownloadCheque.price)
    await message.reply(f"Отлично! Теперь введите цену продукта №{curr_chat.flag_main + 1}:")

@router.message(DownloadCheque.price)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat = dict_chats[message.chat.id]
    try:
        data = await state.get_data()
        curr_chat.products[data["product"]] = int(message.text)
        await state.set_state(DownloadCheque.product)
        curr_chat.flag_main += 1
        if (curr_chat.flag_main == int(data["count_of_positions"])):
            await state.set_state(DownloadCheque.num_people)
            await message.reply(f"Отлично! Нам осталось понять, сколько людей будет скидываться на продукты..")
            curr_chat.flag_main = 0
            await message.reply(f'Сколько людей будет платить за продукт №{curr_chat.flag_main + 1}', reply_markup=kb.makeKeyboardForChoosingNum(message.chat.id, dict_chats))
            # dict_chats[message.chat.id][message.from_user.username]
            return
        await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main + 1}:")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

@router.message(DownloadCheque.num_people)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat = dict_chats[message.chat.id]
    try:
        curr_chat.count_user = int(message.text)
        await state.set_state(DownloadCheque.person)
        await message.reply(f"Выберите, кто будет скидываться за этот продукт.")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

    try:
        DownloadCheque.products[data["product"]] = int(message.text)
        await state.set_state(DownloadCheque.person)
        DownloadCheque.flag_main += 1
        if (DownloadCheque.flag_main == int(data["count_of_positions"])):
            await state.set_state(DownloadCheque.num_people)
            await message.reply(f"Отлично! Нам осталось понять, сколько людей будет скидываться на продукты..")
            DownloadCheque.flag_main = 0
            # dict_chats[message.chat.id][message.from_user.username]
            return
        await message.reply(f"Отлично! Теперь введите название продукта №{DownloadCheque.flag_main + 1}:")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

@router.message(Command('new_list'))
async def cmd_new_list(message: Message):
    pass
    # await check_data(message)

@router.message(Command('remove_list'))
async def cmd_remove_list(message: Message):
    pass
    # await check_data(message)

@router.message()
async def universal(message: Message):
    pass
    # await check_data(message)