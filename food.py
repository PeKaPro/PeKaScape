import random 
from random import choices
import environment as en

class FoodOrDrink():
    def __init__(self, room = None):
        self.room = room if room is not None else random.choice(en.MapFrame.MapFrames)
        
class Food(FoodOrDrink):
    def __init__(self, room = None)