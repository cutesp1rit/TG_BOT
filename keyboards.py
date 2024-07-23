from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def makeKeyboardForChoosingNum(id, dict_chats):
    count_pos = dict_chats[id].get_len()
    choosing_people = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(num)) for num in range(1, count_pos // 3 + 1)], 
                                                [KeyboardButton(text=str(num)) for num in range(count_pos // 3 + 1, (count_pos // 3) * 2 + 1)], 
                                                [KeyboardButton(text=str(num)) for num in range((count_pos // 3) * 2 + 1, count_pos + 1)]],
                                                resize_keyboard=True)
    return choosing_people