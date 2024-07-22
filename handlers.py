from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.pyrogram_functions import get_chat_members
from app.data_bot import bot_token
from app.user import User
from app.states import DownloadCheque
from aiogram.fsm.context import FSMContext
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
        dict_chats[id] = dict()
        chat_members = await get_chat_members(id)
        # убираем бота из списка пользователей
        chat_without_bot = [member for member in chat_members if member != "produc1_manager_bot"]
        for member in chat_without_bot:
            dict_chats[id][member] = User(member, chat_without_bot)


@router.message(CommandStart())
async def cmd_start(message: Message):
    # await check_data(message)
    await message.reply("Привет, сейчас я расскажу, как работает бот...")


@router.message(Command('download_cheque'))
async def cmd_download_cheque(message: Message, state: FSMContext):
    # await check_data(message)
    await message.reply("Напишите количество позиций, которое будет в чеке:")
    await state.set_state(DownloadCheque.count_of_positions)

@router.message(DownloadCheque.count_of_positions)
async def cmd_new_list(message: Message, state: FSMContext):
    try:
        await state.update_data(count_of_positions=int(message.text))
        await state.set_state(DownloadCheque.product)
        await message.reply(f"Отлично! Теперь введите название продукта №{DownloadCheque.flag_main + 1}:")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

@router.message(DownloadCheque.product)
async def cmd_new_list(message: Message, state: FSMContext):
    await state.update_data(product=message.text)
    await state.set_state(DownloadCheque.price)
    await message.reply(f"Отлично! Теперь введите цену продукта №{DownloadCheque.flag_main + 1}:")

@router.message(DownloadCheque.price)
async def cmd_new_list(message: Message, state: FSMContext):
    try:
        data = await state.get_data()
        DownloadCheque.products[data["product"]] = int(message.text)
        await state.set_state(DownloadCheque.product)
        DownloadCheque.flag_main += 1
        if (DownloadCheque.flag_main == int(data["count_of_positions"])):
            await state.set_state(DownloadCheque.num_people)
            await message.reply(f"Отлично! Нам осталось понять, сколько людей будет скидываться на продукты..")
            DownloadCheque.flag_main = 0
            await message.answer(f'Сколько людей будет платить за продукт №{DownloadCheque.flag_main + 1}')
            # dict_chats[message.chat.id][message.from_user.username]
            return
        await message.reply(f"Отлично! Теперь введите название продукта №{DownloadCheque.flag_main + 1}:")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

@router.message(DownloadCheque.num_people)
async def cmd_new_list(message: Message, state: FSMContext):
    try:
        DownloadCheque.count_user = int(message.text)
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