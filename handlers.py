from aiogram import F, Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.telethon_functions import get_chat_members
from app.data_bot import bot_token
from app.user import User
from app.chat import Chat
from app.states import DownloadCheque
from aiogram.fsm.context import FSMContext
from app.cheque import Cheque
import app.keyboards as kb
from aiogram.types import InputFile


# переименовать методы
# какие методы должны быть async
# поля
# скрытие кнопок
# округление чисел
# красивый чек
# сумма в конце

bot = Bot(token=bot_token)
router = Router()
dict_chats = dict()

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
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_chat.last_cheque_ = Cheque(curr_chat.get_users())
    await message.reply("Напишите количество позиций, которое будет в чеке:")
    await state.set_state(DownloadCheque.count_of_positions)

@router.message(DownloadCheque.count_of_positions)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        await state.update_data(count_of_positions=int(message.text))
        curr_chat.count_pos = int(message.text)
        await state.set_state(DownloadCheque.product)
        await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main + 1}:")
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")

@router.message(DownloadCheque.product)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    await state.update_data(product=message.text)
    await state.set_state(DownloadCheque.price)
    await message.reply(f"Отлично! Теперь введите цену продукта №{curr_chat.flag_main + 1}:")

@router.message(DownloadCheque.price)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        await state.update_data(price=int(message.text))
        await state.set_state(DownloadCheque.num_people)
        await message.reply(f"Выберите сколько человек будет скидываться на продукт №{curr_chat.flag_main + 1}:", reply_markup=kb.makeKeyboardForChoosingNum(message.chat.id, dict_chats))
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите целое число, без лишних символов.")


@router.message(DownloadCheque.num_people)
async def cmd_new_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        curr_chat.count_user = int(message.text)
        await state.set_state(DownloadCheque.person)
        await message.reply(f"Выберите, кто будет скидываться за этот продукт (каждого человека отдельным сообщением)", reply_markup=kb.makeKeyboardForChoosingPeople(message.chat.id, dict_chats))
    except Exception:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите/выберите целое ненулевое число, без лишних символов.")


@router.message(DownloadCheque.person)
async def cmd_new_list(message: Message, state: FSMContext):
    data = await state.get_data()
    curr_chat : Chat = dict_chats[message.chat.id]
    # try:
    if not (message.text in curr_chat.get_users()):
        raise Exception
    curr_chat.list_users_products.append(message.text)
    curr_chat.flag_user += 1
    if (curr_chat.flag_user == curr_chat.count_user):
        curr_chat.flag_user = 0
        curr_chat.flag_main += 1
        await curr_chat.last_cheque_.new_product(data["product"], int(data["price"]), curr_chat.list_users_products.copy())
        curr_chat.list_users_products = list()
        if curr_chat.flag_main == curr_chat.count_pos:
            await curr_chat.reset()
            await state.clear()
            await message.reply(f"Ура! Мы получили все данные и уже составляем ваш чек..")
            await curr_chat.last_cheque_.make_cheque(message.chat.id)
            photo = open(f'data_cheque_{message.chat.id}_.png', 'rb')
            await bot.send_photo(message.chat.id, photo)
            return
        await state.set_state(DownloadCheque.product)
        await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main + 1}:")
        return
    await state.set_state(DownloadCheque.person)
    await message.reply(f"Кто еще?", reply_markup=kb.makeKeyboardForChoosingPeople(message.chat.id, dict_chats))
    # except Exception:
    #     await message.reply("Пожалуйста, введите/выберите ник без @ из пользователей этого чата..")


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