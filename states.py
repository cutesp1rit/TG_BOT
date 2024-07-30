from aiogram.fsm.state import State, StatesGroup

class DownloadCheque(StatesGroup):
    count_of_positions = State()
    product = State()
    price = State()
    num_people = State()
    person = State()

class DownloadList(StatesGroup):
    name_of_list = State()
    question = State()
    get_products = State()

class GettingList(StatesGroup):
    get_name = State()

class ModifyLists(StatesGroup):
    chosse_list = State()
    choose_modification = State()
    delete_products = State()