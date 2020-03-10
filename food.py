
import environment as en

# import threading - for future development of potions feature
# import time - likewise

_healing_factors = {"Bread": 3,
                    "Apple": 1,
                    "Fish": 5}


class Food(en.GameObject):
    def __init__(self, room= None):
        super().__init__(room = room)


class Bread(Food):
    def __init__(self, room = None):
        super().__init__(room)
        self.healing_factor = _healing_factors[type(self).__name__]

# potions - increases some stats temporarily
