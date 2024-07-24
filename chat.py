class Chat:
    
    def __init__(self, dict_users):
        self.users = dict_users

        self.flag_main = 0
        self.flag_user = 0
        self.count_pos = 0
        self.count_user = 0
        self.list_users_products = list()
        self.last_cheque_ = 0

    def get_len(self):
        return len(self.users.items())
    
    def get_users(self):
        return list(self.users.keys())
    
    def new_cheque(self, cheque):
        self.last_cheque_ = cheque

    def get_cheque(self):
        if (type(self.last_cheque_) is int):
            return "Вы еще не составляли чеки, для этого используйте команду: ..."
        
        return str(self.last_cheque_)
    
    async def reset(self):
        self.flag_main = 0
        self.flag_user = 0
        self.count_pos = 0
        self.count_user = 0
        self.list_users_products = list()