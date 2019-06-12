import random 
from random import choices
import environment as en

import threading
import time

class Food(en.GameObject):
    def __init__(self, room = None):
        super().__init__(room=room)
        
        #few types of food - each heals different
        
        #potions - increases  
        
