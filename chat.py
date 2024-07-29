class Chat:
    def __init__(self, dict_users):
        self.users_ = dict_users

        self.flag_main_ = 0
        self.flag_user_ = 0
        self.count_pos_ = 0
        self.count_user_ = 0
        self.list_users_products_ = list()
        self.last_cheque_ = 0
        self.dict_for_shop_lists_ = dict()

    def get_len(self):
        return len(self.users_.items())
    
    def get_users(self):
        return list(self.users_.keys())
    
    def new_cheque(self, cheque):
        self.last_cheque_ = cheque

    def get_cheque(self):
        if (type(self.last_cheque_) is int):
            return "Вы еще не составляли чеки, для этого используйте команду: /download_cheque"
        return self.last_cheque_
    
    def check_cheque(self):
        return not(type(self.last_cheque_) is int)
    
    async def reset(self):
        self.flag_main_ = 0
        self.flag_user_ = 0
        self.count_pos_ = 0
        self.count_user_ = 0
        self.list_users_products_ = list()