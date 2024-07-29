import pandas as pd
import dataframe_image as dfi

class Cheque:
    def __init__(self, users, creater):
        self.users_ = users
        self.creater_ = creater
        self.dict_money_ = dict()
        self.products_ = list()
        for user in users:
            self.dict_money_[str(user)] = list()

    async def new_product(self, product, price, users):
        self.products_.append(product)
        divided_price = price / len(users)
        tmp_dict = dict() # для контроля входящих одинаковых ников пользователей
        for user in users:
            if (tmp_dict.get(str(user), -1) == -1):
                self.dict_money_[str(user)].append(round(divided_price, 2))
                tmp_dict[str(user)] = 1
            else: # здесь 1
                self.dict_money_[str(user)][-1] += round(divided_price, 2)
        for user in self.users_:
            if not (user in users):
                self.dict_money_[str(user)].append(0)

    async def make_cheque(self, chat_id):
        # добавляем сумму в конце
        for member in self.dict_money_.items():
            self.dict_money_[member[0]].append(sum(member[1]))
        self.products_.append("Итог")
        self.cheque_ = pd.DataFrame(self.dict_money_)
        self.cheque_.index = self.products_
        dfi.export(self.cheque_, f'data_cheque_{chat_id}_.png')

    def get_creater(self):
        return self.creater_
    
    def get_cheque(self):
        return self.dict_money_