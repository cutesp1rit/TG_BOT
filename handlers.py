from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.telethon_functions import get_chat_members
from app.user import User
from app.chat import Chat
from app.states import DownloadCheque
from aiogram.fsm.context import FSMContext
from app.cheque import Cheque
import app.keyboards as kb
from aiogram.types import FSInputFile
from app.exceptions import IncorrectData
from os import remove


# добавить смайлики и красоту в целом
# написать свои исключения -- DONE
# переименовать методы -- DONE
# какие методы должны быть async - ?
# поля -- DONE
# скрытие кнопок -- DONE
# округление чисел -- DONE
# красивый чек -- DONE
# сумма в конце -- DONE
# привязать последний чек к user -- DONE
# добавить систему долгов -- DONE
# сделать команду получить последний чек -- DONE
# отдельная папка для чеков - ?
# поченить бота если несколько человек одиноковых -- DONE
# возможно стоит добавить команду help
# прописать логи
# доделать команды со списком

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
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_chat.new_cheque(Cheque(curr_chat.get_users(), message.from_user.username))
    curr_chat.users_[message.from_user.username].new_cheque(curr_chat.last_cheque_)
    await message.reply("Напишите количество позиций, которое будет в чеке:")
    await state.set_state(DownloadCheque.count_of_positions)

@router.message(DownloadCheque.count_of_positions)
async def get_count_of_positions(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        await state.update_data(count_of_positions=int(message.text))
        curr_chat.count_pos_ = int(message.text)
        await state.set_state(DownloadCheque.product)
        await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main_ + 1}:")
    except ValueError:
        await message.reply(f"Некорректные данные, пожалуйста, введите целое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"Произошла непредвиденная ошибка: {ex}")

@router.message(DownloadCheque.product)
async def get_name_of_product(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    await state.update_data(product=message.text)
    await state.set_state(DownloadCheque.price)
    await message.reply(f"Отлично! Теперь введите цену продукта №{curr_chat.flag_main_ + 1}:")

@router.message(DownloadCheque.price)
async def get_price(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        await state.update_data(price=int(message.text))
        await state.set_state(DownloadCheque.num_people)
        await message.reply(f"Выберите сколько человек будет скидываться на продукт №{curr_chat.flag_main_ + 1}:", reply_markup=kb.makeKeyboardForChoosingNum(message.chat.id, dict_chats))
    except ValueError:
        await message.reply(f"Некорректные данные, пожалуйста, введите целое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"Произошла непредвиденная ошибка: {ex}")


@router.message(DownloadCheque.num_people)
async def get_num_of_people(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        if int(message.text) == 0:
            raise ValueError
        curr_chat.count_user_ = int(message.text)
        await state.set_state(DownloadCheque.person)
        await message.reply(f"Выберите, кто будет скидываться за этот продукт (каждого человека отдельным сообщением)", reply_markup=kb.makeKeyboardForChoosingPeople(message.chat.id, dict_chats))
    except ValueError:
        await message.reply("Вы ввели некорректные данные, пожалуйста, введите/выберите целое ненулевое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"Произошла непредвиденная ошибка: {ex}")


@router.message(DownloadCheque.person)
async def get_names_of_people(message: Message, state: FSMContext):
    data = await state.get_data()
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        if not (message.text in curr_chat.get_users()):
            raise IncorrectData
        curr_chat.list_users_products_.append(message.text)
        curr_chat.flag_user_ += 1
        if (curr_chat.flag_user_ == curr_chat.count_user_):
            curr_chat.flag_user_ = 0
            curr_chat.flag_main_ += 1
            await curr_chat.last_cheque_.new_product(data["product"], int(data["price"]), curr_chat.list_users_products_.copy())
            curr_chat.list_users_products_ = list()
            if curr_chat.flag_main_ == curr_chat.count_pos_:
                await curr_chat.reset()
                await state.clear()
                await message.reply(f"Ура! Мы получили все данные и уже составляем ваш чек..")
                await curr_chat.last_cheque_.make_cheque(message.chat.id)
                await message.answer_photo(photo=FSInputFile(f'data_cheque_{message.chat.id}_.png'))
                remove(f'data_cheque_{message.chat.id}_.png')
                cur_user : User = curr_chat.users_[(curr_chat.get_cheque()).get_creater()]
                await cur_user.calculate_other_debts()
                for user in cur_user.list_without_user_:
                    await curr_chat.users_[user].calculate_own_debts(curr_chat.get_cheque())
                return
            await state.set_state(DownloadCheque.product)
            await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main_ + 1}:")
            return
        await state.set_state(DownloadCheque.person)
        await message.reply(f"Кто еще?", reply_markup=kb.makeKeyboardForChoosingPeople(message.chat.id, dict_chats))
    except IncorrectData:
        await message.reply("Пожалуйста, введите/выберите ник без @ из пользователей этого чата..")
    except Exception as ex:
        await message.reply(f"Произошла непредвиденная ошибка: {ex}")

@router.message(Command('get_my_debts'))
async def cmd_get_my_debts(message: Message):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_user : User = curr_chat.users_[message.from_user.username]
    await message.reply(curr_user.get_own_debts())
    

@router.message(Command('get_other_debts'))
async def cmd_get_other_debts(message: Message):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_user : User = curr_chat.users_[message.from_user.username]
    await message.reply(curr_user.get_other_debts())

@router.message(Command('new_list'))
async def cmd_new_list(message: Message):
    await check_data(message)

@router.message(Command('get_lists'))
async def cmd_get_lists(message: Message):
    await check_data(message)

@router.message(Command('get_last_cheque'))
async def cmd_get_last_cheque(message: Message):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    if (curr_chat.check_cheque()):
        creater = await curr_chat.get_cheque().get_cheque_image(message.chat.id)
        await message.answer_photo(photo=FSInputFile(f'data_cheque_{message.chat.id}_.png'))
        remove(f'data_cheque_{message.chat.id}_.png')
        await message.answer(f"Его создатель: @{creater}")
    else:
        await message.reply("Вы еще не составляли чеки, для этого используйте команду: /download_cheque")

@router.message(Command('remove_list'))
async def cmd_remove_list(message: Message):
    await check_data(message)

@router.message()
async def universal(message: Message):
    await check_data(message)