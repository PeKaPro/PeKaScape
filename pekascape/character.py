"""
Module defining basic agents of the game
1. Character as a very generic class
2. Player as a class meant to represent human player
3. Monster as a class of NPC enemies
"""
from environment import MapFrame
from pekascape import base
from pekascape import behaviour
from pekascape import items
from pekascape.interface import PlayerGameText

# future todo: move printed texts into special enums in base modules


class Character(base.GameObject):
    Characters = list()
    
    def __init__(self, room=None, health=100, attack=1, defence=1):
        Character.Characters.append(self)
        super().__init__(room)
        self.health = health
        self.attack = attack
        self.defence = defence


class Player(Character):
    """
    Player class - instance of this class is meant to be controlled by real world player
    """
    Players = list()

    def __init__(self, name:str , room: MapFrame, health=100, attack=1, defence=1):
        Player.Players.append(self)
        super().__init__(room, health, attack, defence)
        self.name = name
        print(f"Hey There, I am new character called {self.name}.")
        self.inventory = list()
        self.wielded_weapon = None
        self.room.players.append(self)
        self.alive = 1
        
    def pickup(self, item):
        if not self.alive:
            print(PlayerGameText.DEAD_INVOKE_ACTION)
            return
        if len(self.inventory) == 3:
            print(f"I cant pick up anything, I am fully loaded.\nDrop something first.")
            return
        if item not in [x.name for x in self.room.items]:
            print(f"I cant pick up {item} as its not in this room.\n")
            return
        if item in [x.name for x in self.room.items]:
            item = [x for x in self.room.items if x.name == item][0]
            # self.inventory.append([x for x in self.room.items if x.name==item][0])
            self.inventory.append(item)
            # self.room.items.remove([x for x in self.room.items if x.name==item][0])
            self.room.items.remove(item)
            print(f"I have picked up {item.name}.")
            if isinstance(item, items.Weapon):
                print(f"It has bonus {item.att_bonus} - consider wielding it.")
                
    def drop(self, item):
        if item not in [x.name for x in self.inventory]:
            print(f"I cant drop something I dont have, check your inventory again.")
            return
        self.room.items.append([x for x in self.inventory if x.name == item][0])
        self.inventory.remove([x for x in self.inventory if x.name == item][0])
        
    def see(self):
        for direction in self.room.neighbours.keys():
            if self.room.neighbours.get(direction):
                print(f"There is door to the {direction} in this room.")
        for monster in self.room.monsters:
            print(f"There is {monster.name} in the room.")
        print("\n")
        for item in self.room.items:
            print(f"There is {item.name} in the room.")
       
    def fight(self, other):
        if other not in [monster.name for monster in self.room.monsters]:
            print(f"There is not monster named {other} in this room.")
        else:
            print("Fight is on!")
            behaviour.Battle.fight(self, [monster for monster in self.room.monsters if monster.name == other][0])
        
    def wield(self, item):
        if item not in [x.name for x in self.inventory]:
            print("I cannot wield something I dont have.")
            return
        self.wielded_weapon = [x for x in self.inventory if x.name == item][0]
        self.attack += self.wielded_weapon.att_bonus
        self.inventory.remove([x for x in self.inventory if x.name == item][0])
        
    def go(self, direction):
        target = self.room.neighbours.get(direction)
        if not target:
            print(f"There is no room in direction of {direction}.")
        else:
            target.players.append(self)
            self.room.players.remove(self)
            self.room = target
    

class Monster(Character):
    Monsters = list()
        
    def __init__(self, name=None, room=None, health=100, attack=1, defence=1):
        Monster.Monsters.append(self)
        super().__init__(room, health, attack, defence)
        self.name = name if name is not None else "Monster"+str(len(Monster.Monsters))
        print(f"Hey There, I am new monster called {self.name}.")
        self.inventory = list()
        self.room.monsters.append(self)
            
    def fight(self, other):
        pass

    def __del__(self):
        print(f"Deleting {self.name}")
        while self.inventory:
            self.room.items.append(self.inventory.pop())
        self.room.monsters.remove(self)     # remove from the room
        type(self).Monsters.remove(self)    # remove from monsters list
        Character.Characters.remove(self)   # remove from characters list
