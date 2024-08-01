from app.cheque import Cheque

class User:
    def __init__(self, name, list_of_users):
        self.name_ = name
        list_without_user = [member for member in list_of_users if str(member) != str(name)]
        self.list_without_user_ = list_without_user
        self.other_debts_ = dict()
        self.own_debts_ = dict()
        self.last_cheque_ = 0
        for person in list_without_user:
            self.other_debts_[person] = 0.0
            self.own_debts_[person] = 0.0

    async def calculate_other_debts(self):
        for user in self.last_cheque_.get_cheque().items():
            if user[0] != self.name_:
                self.other_debts_[user[0]] += user[1][-1]

    async def calculate_own_debts(self, cheque : Cheque):
        for user in cheque.get_cheque().items():
            if user[0] == self.name_:
                self.own_debts_[cheque.get_creater()] += user[1][-1]

    def get_list_without_user(self):
        return self.list_without_user_

    def get_own_debts(self):
        res = f"<b>@{self.name_} должен:</b>\n\n"
        for i in self.own_debts_.items():
            res += f"@{i[0]}: {i[1]}\n"
        res += f"<u>всего</u>: {sum(self.own_debts_.values())}"
        return res
        
    def get_other_debts(self):
        res = f"<b>В долгу у @{self.name_}:</b>\n\n"
        for i in self.other_debts_.items():
            res += f"@{i[0]}: {i[1]}\n"
        res += f"<u>всего</u>: {sum(self.other_debts_.values())}"
        return res

    def new_other_debts(self, person, money):
        self.other_debts_[person] += money

    def new_own_debts(self, person, money):
        self.own_debts_[person] += money

    def new_cheque(self, cheque):
        self.last_cheque_ = cheque

    async def remove_other_debt(self, name, num):
        self.other_debts_[name] -= num
    
    async def remove_own_debt(self, name, num):
        self.own_debts_[name] -= num