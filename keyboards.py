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

current_date = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Использовать текущую дату")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)

yes_or_no = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)

stop = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="/stop")]],
                                                resize_keyboard=True,
                                                one_time_keyboard=True)