import pandas as pd

class Cheque:
    def __init__(self, users):
        self.users_ = users
        self.dict_money_ = dict()
        self.products_ = list()
        for user in users:
            self.dict_money_[str(user)] = list()

    async def new_product(self, product, price, users):
        self.products_.append(product)
        divided_price = price / len(users)
        for user in users:
            self.dict_money_[str(user)].append(divided_price)
        for user in self.users_:
            if not (user in users):
                self.dict_money_[str(user)].append(0)

    async def make_cheque(self):
        self.cheque_ = pd.DataFrame(self.dict_money_)
        self.cheque_.index = self.products_
        print(self.cheque_)
        return str(self.cheque_)