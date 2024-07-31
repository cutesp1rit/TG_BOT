class Product:
    def __init__(self, name, mark=False):
        self.name_ = name
        self.mark_ = mark
    
    def get_mark(self):
        return self.mark_

    def get_name(self):
        return self.name_
    
    def __str__(self):
        return self.name_