from aiogram.fsm.state import State, StatesGroup

class DownloadCheque(StatesGroup):
    flag_main = 0
    flag_user = 0
    count_user = 0

    products = dict()
    list_users_products = list()

    count_of_positions = State()
    product = State()
    price = State()
    num_people = State()
    person = State()