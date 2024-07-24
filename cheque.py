class Cheque:
    def __init__(self, users):
        self.users_ = users
        self.dict_money_ = dict()
        self.products_ = list()
        for user in users:
            self.dict_money_[str(user)] = list()

    def new_product(self, product, price, users):
        self.products_.append(product)
        divided_price = price / len(users)
        for user in users:
            self.dict_money_[str(user)].append(divided_price)