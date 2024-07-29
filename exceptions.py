class IncorrectData(Exception):
    def __init__(self, *args):
        if args:
            self.message_ = args[0]
        else:
            self.message_ = None
    
    def __str__(self):
        if self.message_:
            return f"{self.message_}"
        else:
            return f"Некорректные данные"