class User:
    def __init__(self, name, list_of_users):
        self.name_ = name
        list_without_user = [member for member in list_of_users if str(member) != str(name)]
        self.other_debts_ = dict()
        self.own_debts_ = dict()
        for person in list_without_user:
            self.other_debts_[person] = 0.0
            self.own_debts_[person] = 0.0

    def get_own_debts(self):
        res = f"@{self.name_} должен:\n"
        for i in self.own_debts_.items():
            res += f"@{i[0]}: {i[1]}\n"
        res += f"всего: {sum(self.own_debts_.values())}"
        return res
        
    def get_other_debts(self):
        res = f"в долгу у @{self.name_}:\n"
        for i in self.other_debts_.items():
            res += f"@{i[0]}: {i[1]}\n"
        res += f"всего: {sum(self.other_debts_.values())}"
        return res

    def new_other_debts(self, person, money):
        self.other_debts_[person] += money

    def new_own_debts(self, person, money):
        self.own_debts_[person] += money