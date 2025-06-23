class Item:
    def __init__(self, name, stackable, quantity=1):
        self.name = name
        self.quantity = quantity
        self.stackable = stackable