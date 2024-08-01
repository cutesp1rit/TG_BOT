from aiogram import Router, F
from aiogram.types import Message, FSInputFile, ForceReply, CallbackQuery
from aiogram.filters import CommandStart, Command
from app.telethon_functions import get_chat_members
from app.user import User
from app.chat import Chat
from app.states import DownloadCheque, DownloadList, GettingList, ModifyLists, RemoveDebt
from aiogram.fsm.context import FSMContext
from app.cheque import Cheque
import app.keyboards as kb
from aiogram.enums import ParseMode
from app.exceptions import IncorrectData
from os import remove
from app.product import Product
import app.long_messages as lm


# добавить смайлики и красоту в целом
# какие методы должны быть async - ?
# отдельная папка для чеков - ?
# возможно стоит добавить команду help
# прописать логи
# выводить список, чтобы зачеркивать -- DONE
# убрать стоп -- DONE
# сделать reply_markup с ответом на сообщение - ?
# возможно сделать ответ с помощью inline кнопок -- DONE
# inline кнопку для даты -- DONE

router = Router()
dict_chats = dict()

async def check_data(message: Message):
    id = message.chat.id
    if (type(dict_chats.get(id, -1)) is int):
        dict_tmp = dict()
        chat_members = await get_chat_members(id)
        # убираем ботов из списка пользователей
        chat_without_bot = [member for member in chat_members if member[-3:] != "bot"]
        for member in chat_without_bot:
            dict_tmp[member] = User(member, chat_without_bot)
        dict_chats[id] = Chat(dict_tmp)

@router.message(CommandStart())
async def cmd_start(message: Message):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    if (len(curr_chat.get_users()) == 1):
        await message.answer(lm.start_message_for_user, parse_mode=ParseMode.HTML)
    else:
        await message.answer(lm.start_message_for_chat, parse_mode=ParseMode.HTML)

@router.message(Command('help'))
async def cmd_download_cheque(message: Message, state: FSMContext):
    await check_data(message)
    await message.answer(lm.help_message, parse_mode=ParseMode.HTML)

@router.message(Command('download_cheque'))
async def cmd_download_cheque(message: Message, state: FSMContext):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_chat.new_cheque(Cheque(curr_chat.get_users(), message.from_user.username))
    curr_chat.users_[message.from_user.username].new_cheque(curr_chat.last_cheque_)
    await message.reply("Напишите количество позиций, которое будет в чеке 🧾:")
    await state.set_state(DownloadCheque.count_of_positions)

@router.message(Command('get_my_debts'))
async def cmd_get_my_debts(message: Message):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_user : User = curr_chat.users_[message.from_user.username]
    await message.reply(curr_user.get_own_debts(), parse_mode=ParseMode.HTML)
    

@router.message(Command('get_other_debts'))
async def cmd_get_other_debts(message: Message):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    curr_user : User = curr_chat.users_[message.from_user.username]
    await message.reply(curr_user.get_other_debts(), parse_mode=ParseMode.HTML)

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
        await message.reply("❗️ Вы еще не составляли чеки, для этого используйте команду: /download_cheque")

@router.message(Command('new_list'))
async def cmd_new_list(message: Message, state: FSMContext):
    await check_data(message)
    await message.reply("Напишите название списка 📋:", reply_markup=kb.current_date_inline)
    await state.set_state(DownloadList.name_of_list)

@router.message(Command('remove_debt'))
async def cmd_remove_debt(message: Message, state: FSMContext):
    await check_data(message)
    curr_chat : Chat = dict_chats[message.chat.id]
    await state.update_data(user=message.from_user.username)
    await message.reply("Выберите с какого пользователя вы бы хотели снять долг 💰", reply_markup=kb.makeKeyboardForChoosingPeopleWithoutUser(curr_chat.users_[message.from_user.username].get_list_without_user()))
    await state.set_state(RemoveDebt.choose_person)

@router.message(Command('get_lists'))
async def cmd_get_lists(message: Message, state: FSMContext):
    await check_data(message)
    if (len(dict_chats[message.chat.id].get_dict_for_shop_lists_name()) == 0):
        await message.reply("Вы еще не создавали списки, для этого воспользуйтесь командой /new_list")
        return
    await message.reply("Выберите какой из списков вы бы хотели посмотреть 👀:", reply_markup=kb.makeKeyboardForGettingLists(dict_chats[message.chat.id]))
    await state.set_state(GettingList.get_name)

@router.message(Command('modify_lists'))
async def cmd_modify_lists(message: Message, state: FSMContext):
    await check_data(message)
    await message.reply("Выберите какой из списков вы бы хотели изменить ✍🏻:", reply_markup=kb.makeKeyboardForGettingLists(dict_chats[message.chat.id]))
    await state.set_state(ModifyLists.choose_list)

@router.message(GettingList.get_name)
async def gl_get_name(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        if not (message.text in curr_chat.get_dict_for_shop_lists_name()):
            raise IncorrectData
        if (await curr_chat.get_len_list(message.text) == 0):
            await message.reply(f"Этот список еще пуст, для его заполнения воспользуйтесь командой: /modify_lists")
        else:
            list = await curr_chat.get_list(message.text)
            await message.reply(f'Список 📋 <b>"{message.text}"</b>:\n\n{list}', parse_mode=ParseMode.HTML)
        await state.clear()
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите список из предложенных кнопками, других нет..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(ModifyLists.choose_list)
async def ml_get_name(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        if not (message.text in curr_chat.get_dict_for_shop_lists_name()):
            raise IncorrectData
        await state.update_data(name=message.text)
        await message.reply("Отлично! Теперь выберите, что конкретно вы бы хотели сделать с этим списком.", reply_markup=kb.options_for_modification)
        await state.set_state(ModifyLists.choose_modification)
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите список из предложенных кнопками, других нет..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(ModifyLists.choose_modification)
async def ml_get_opt(message: Message, state: FSMContext):
    opt_mod = ["🗑 удалить список", "🧹 очистить список", "🗑 удалить некоторые элементы из списка", "✔️ добавить некоторые элементы в список", "✏️ зачеркнуть купленные продукты"]
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    try:
        if not (str(message.text).lower() in opt_mod):
            raise IncorrectData
        # обработка полученных данных
        low_message = str(message.text).lower()
        if low_message == opt_mod[0]:
            await curr_chat.delete_list(data["name"])
            await message.reply("Мы успешно удалили данный список!")
        elif low_message == opt_mod[1]:
            await curr_chat.clear_list(data["name"])
            await message.reply("Мы успешно очистили данный список!")
        elif low_message == opt_mod[2]:
            list = await curr_chat.get_list(data["name"])
            await message.answer(f"Вот список:")
            await message.answer(f'Список 📋 <b>"{data["name"]}"</b>:\n\n{list}', parse_mode=ParseMode.HTML)
            await message.reply("Последовательно по сообщению вводите название каждого продукта, которое хотите удалить. Для остановки воспользуйтесь кнопкой.", reply_markup=kb.stop_inline)
            await state.set_state(ModifyLists.delete_products)
        elif low_message == opt_mod[3]:
            await state.set_state(DownloadList.choose_option)
            await message.reply("Выберите как вы собираетесь создать список:", reply_markup=kb.options_elementwise_or_not)
        else:
            list = await curr_chat.get_list(data["name"])
            await message.answer(f'Список <b>"{data["name"]}"</b>:\n\n{list}', parse_mode=ParseMode.HTML)
            await state.set_state(ModifyLists.cross_out_product)
            await message.reply("Выберите как вы собираетесь зачеркнуть элементы списка:", reply_markup=kb.options_elementwise_or_not)
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите опцию из предложенных кнопками, других нет..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(ModifyLists.cross_out_product)
async def dl_ch_opt(message: Message, state: FSMContext):
    arr_opt = ["вводить продукты поэлементно", "ввести все одним списком-сообщением"]
    try:
        if not (message.text.lower() in arr_opt):
            raise IncorrectData
        if (message.text.lower() == "вводить продукты поэлементно"):
            await state.set_state(ModifyLists.get_products)
            await message.reply("Хорошо, последовательно по сообщению вводите название каждого продукта. Для остановки воспользуйтесь кнопкой.", reply_markup=kb.stop_inline)
        else:
            await state.set_state(ModifyLists.get_list)
            await message.reply("Хорошо, тогда одним сообщением отправьте ваш список, чтобы каждый продукт был на отдельной строке. Пример:")
            await message.answer('Помидоры\nОгурцы\nХлеб\n...')
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите опцию из предложенных кнопками, других нет..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(ModifyLists.get_list)
async def dl_get_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    try:
        new_list = [product.lower() for product in message.text.split('\n')]
        if (type(curr_chat.dict_for_shop_lists_.get(data["name"], -1)) is int):
            await message.reply("Готово!")
            return
        for product in new_list:
            for thing in curr_chat.dict_for_shop_lists_[data["name"]]:
                if thing.get_name() == product.lower():
                    thing.mark_ = not(thing.get_mark())
                    break
        await message.reply(f"Все найденные продукты были зачеркнуты!")
        await state.clear()
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(ModifyLists.get_products)
async def dl_question(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    product = message.text.lower()
    for thing in curr_chat.dict_for_shop_lists_[data["name"]]:
        if thing.get_name() == product.lower():
            thing.mark_ = not(thing.get_mark())
            await message.reply("Что еще?")
            return
    await message.reply("К сожалению, мы не нашли это в списке продуктов :(\nЧто еще?", reply_markup=kb.stop_inline)

@router.message(ModifyLists.delete_products)
async def ml_del_prod(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    try:
        if not(message.text.lower() in curr_chat.dict_for_shop_lists_[data["name"]]):
            raise IncorrectData
        curr_chat.dict_for_shop_lists_[data["name"]].remove(message.text.lower())
        await message.reply("Что еще?")
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите элемент из списка, других нет..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(DownloadCheque.count_of_positions)
async def get_count_of_positions(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    try:
        if (int(message.text) == 0):
            raise ValueError
        await state.update_data(count_of_positions=int(message.text))
        curr_chat.count_pos_ = int(message.text)
        await state.set_state(DownloadCheque.product)
        await message.reply(f"Отлично! Теперь введите название продукта №{curr_chat.flag_main_ + 1}:")
    except ValueError:
        await message.reply(f"❗️ Некорректные данные, пожалуйста, введите целое ненулевое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

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
        await message.reply(f"❗️ Некорректные данные, пожалуйста, введите целое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")


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
        await message.reply("❗️ Вы ввели некорректные данные, пожалуйста, введите/выберите целое ненулевое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")


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
                await message.reply(f"Ура! 👏 Мы получили все данные и уже составляем ваш чек..")
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
        await message.reply("❗️ Пожалуйста, введите/выберите ник без @ из пользователей этого чата..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(RemoveDebt.choose_person)
async def rd_choose_person(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    try:
        if not (message.text in curr_chat.users_[data["user"]].get_list_without_user()):
            raise IncorrectData
        await state.update_data(debtor=message.text)
        await state.set_state(RemoveDebt.get_num)
        await message.reply("Отлично! Теперь введите размер какого долга 💰 (число) с него вы собираетесь снять:")
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите ник без @ из пользователей этого чата, а также не себя..", reply_markup=kb.makeKeyboardForChoosingPeopleWithoutUser(curr_chat.users_[data["user"]].get_list_without_user()))
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(RemoveDebt.get_num)
async def rd_get_num(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    try:
        await curr_chat.users_[data["user"]].remove_other_debt(data["debtor"], int(message.text))
        await curr_chat.users_[data["debtor"]].remove_own_debt(data["user"], int(message.text))
        await message.reply(f"Долг был снят!")
        await state.clear()
    except ValueError:
        await message.reply("❗️ Вы ввели некорректные данные, пожалуйста, введите/выберите целое число, без лишних символов.")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(DownloadList.name_of_list)
async def get_name_of_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    if (not(type(curr_chat.dict_for_shop_lists_.get(message.text, -1)) is int)):
        await message.reply("❗️ Список с таким именем уже существует! Пожалуйста, введите другое название:")
        return
    if (message.text == "Использовать текущую дату в качестве названия"):
        today = message.date
        if (not(type(curr_chat.dict_for_shop_lists_.get("{}.{}.{}".format(today.day, today.month, today.year), -1)) is int)):
            await message.reply("❗️ Список с таким именем уже существует! Пожалуйста, введите другое название:")
            return
        curr_chat.dict_for_shop_lists_["{}.{}.{}".format(today.day, today.month, today.year)] = list()
        await state.update_data(name="{}.{}.{}".format(today.day, today.month, today.year))
    else:
        curr_chat.dict_for_shop_lists_[message.text] = list()
        await state.update_data(name=message.text)
    await state.set_state(DownloadList.question)
    await message.reply("Отлично! Хотите сейчас добавить продукты в него?", reply_markup=kb.yes_or_no)

@router.message(DownloadList.question)
async def dl_question(message: Message, state: FSMContext):
    if (message.text.title() != "Да" and message.text.title() != "Нет"):
        await message.reply('❗️ Пожалуйста, воспользуйтесь кнопками или напишите "Да"/"Нет"..', reply_markup=kb.yes_or_no)
    else:
        if (message.text.title() == "Нет"):
            await message.reply("Хорошо, вернули вас в главное меню")
            await state.clear()
        else:
            await state.set_state(DownloadList.choose_option)
            await message.reply("Выберите как вы собираетесь создать список:", reply_markup=kb.options_elementwise_or_not)

@router.message(DownloadList.choose_option)
async def dl_ch_opt(message: Message, state: FSMContext):
    arr_opt = ["вводить продукты поэлементно", "ввести все одним списком-сообщением"]
    try:
        if not (message.text.lower() in arr_opt):
            raise IncorrectData
        if (message.text.lower() == "вводить продукты поэлементно"):
            await state.set_state(DownloadList.get_products)
            await message.reply("Хорошо, последовательно по сообщению вводите название каждого продукта. Для остановки воспользуйтесь кнопкой.", reply_markup=kb.stop_inline)
        else:
            await state.set_state(DownloadList.get_list)
            await message.reply("Хорошо, тогда одним сообщением отправьте ваш список, чтобы каждый продукт был на отдельной строке. Пример:")
            await message.answer('Помидоры\nОгурцы\nХлеб\n...')
    except IncorrectData:
        await message.reply("❗️ Пожалуйста, введите/выберите опцию из предложенных кнопками, других нет..")
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.message(DownloadList.get_list)
async def dl_get_list(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    try:
        new_list = [Product(product.lower()) for product in message.text.split('\n')]
        if (type(curr_chat.dict_for_shop_lists_.get(data["name"], -1)) is int):
            curr_chat.dict_for_shop_lists_[data["name"]] = list()
        curr_chat.dict_for_shop_lists_[data["name"]] += new_list
        await message.reply(f"Готово!")
        await state.clear()
    except Exception as ex:
        await message.reply(f"❗️ Произошла непредвиденная ошибка: {ex}")

@router.callback_query(F.data == "stop")
async def cq_stop(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Ввод окончен.")
    await callback.message.reply("Хорошо, вернули вас в главное меню")
    await state.clear()

@router.callback_query(F.data == "data989" and DownloadList.name_of_list)
async def get_name_of_list(callback: CallbackQuery, state: FSMContext):
    message = callback.message
    curr_chat : Chat = dict_chats[message.chat.id]
    today = message.date
    if (not(type(curr_chat.dict_for_shop_lists_.get("{}.{}.{}".format(today.day, today.month, today.year), -1)) is int)):
        await message.reply("❗️ Список с таким именем уже существует! Пожалуйста, введите другое название:")
        return
    curr_chat.dict_for_shop_lists_["{}.{}.{}".format(today.day, today.month, today.year)] = list()
    await state.update_data(name="{}.{}.{}".format(today.day, today.month, today.year))
    await callback.answer("Сегодня {}.{}.{}".format(today.day, today.month, today.year))
    await state.set_state(DownloadList.question)
    await message.reply("Отлично! Хотите сейчас добавить продукты в него?", reply_markup=kb.yes_or_no)

@router.message(DownloadList.get_products)
async def dl_question(message: Message, state: FSMContext):
    curr_chat : Chat = dict_chats[message.chat.id]
    data = await state.get_data()
    curr_chat.dict_for_shop_lists_[data["name"]].append(Product(message.text.lower()))
    await message.reply("Что еще?")
    

@router.message()
async def universal(message: Message):
    await check_data(message)