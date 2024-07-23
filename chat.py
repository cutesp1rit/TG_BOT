class Chat:
    
    def __init__(self, dict_users):
        self.users = dict_users

        self.flag_main = 0
        self.flag_user = 0
        self.count_pos = 0
        self.count_user = 0
        self.products = dict()
        self.list_users_products = list()

    def get_len(self):
        return len(self.users.items())
    
    def get_users(self):
        return list(self.users.keys())