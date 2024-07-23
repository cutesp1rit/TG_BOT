from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.states import DownloadCheque

#choosing_people = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=str(num)) for num in range(1, DownloadCheque.count_pos // 3 + 1)], 
#                                                [KeyboardButton(text=str(num)) for num in range(DownloadCheque.count_pos // 3 + 1, (DownloadCheque.count_pos // 3) * 2 + 1)], 
#                                                [KeyboardButton(text=str(num)) for num in range((DownloadCheque.count_pos // 3) * 2 + 1, DownloadCheque.count_pos + 1)]],
#                                               resize_keyboard=True)