from aiogram.fsm.state import State, StatesGroup

class DownloadCheque(StatesGroup):
    count_of_positions = State()
    product = State()
    price = State()
    num_people = State()
    person = State()