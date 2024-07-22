from aiogram.fsm.state import State, StatesGroup

class DownloadCheque(StatesGroup):
    flag = 0
    products = dict()

    count_of_positions = State()
    product = State()
    price = State()
    finish = State()