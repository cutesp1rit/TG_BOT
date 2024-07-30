from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def makeKeyboardForChoosingNum(id, dict_chats):
    count_pos = dict_chats[id].get_len()
    choosing_num = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(num)) for num in range(1, count_pos // 3 + 1)], 
                                                [KeyboardButton(text=str(num)) for num in range(count_pos // 3 + 1, (count_pos // 3) * 2 + 1)], 
                                                [KeyboardButton(text=str(num)) for num in range((count_pos // 3) * 2 + 1, count_pos + 1)]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)
    return choosing_num

def makeKeyboardForChoosingPeople(id, dict_chats):
    count_pos = dict_chats[id].get_len()
    persons = dict_chats[id].get_users()
    choosing_people = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(persons[i - 1])) for i in range(1, count_pos // 3 + 1)], 
                                                [KeyboardButton(text=str(persons[i - 1])) for i in range(count_pos // 3 + 1, (count_pos // 3) * 2 + 1)], 
                                                [KeyboardButton(text=str(persons[i - 1])) for i in range((count_pos // 3) * 2 + 1, count_pos + 1)]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)
    return choosing_people

def makeKeyboardForChoosingPeopleWithoutUser(persons):
    count_pos = len(persons)
    choosing_people = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(persons[i - 1])) for i in range(1, count_pos // 3 + 1)], 
                                                [KeyboardButton(text=str(persons[i - 1])) for i in range(count_pos // 3 + 1, (count_pos // 3) * 2 + 1)], 
                                                [KeyboardButton(text=str(persons[i - 1])) for i in range((count_pos // 3) * 2 + 1, count_pos + 1)]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)
    return choosing_people

def makeKeyboardForGettingLists(chat):
    chat_lists_name = list(chat.get_dict_for_shop_lists_name())
    length = len(chat_lists_name)
    lists = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(chat_lists_name[i - 1])) for i in range(1, length // 3 + 1)], 
                                                [KeyboardButton(text=str(chat_lists_name[i - 1])) for i in range(length // 3 + 1, (length // 3) * 2 + 1)], 
                                                [KeyboardButton(text=str(chat_lists_name[i - 1])) for i in range((length // 3) * 2 + 1, length + 1)]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)
    return lists

current_date = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Использовать текущую дату")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)

yes_or_no = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)

stop = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/stop")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)

options_for_modification = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Удалить список")], [KeyboardButton(text="Очистить список")],
                                                         [KeyboardButton(text="Удалить некоторые элементы из списка")], [KeyboardButton(text="Добавить некоторые элементы в список")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)