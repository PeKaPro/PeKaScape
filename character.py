import environment as en
import weapon as we
from base import PlayerGameText

# future todo: move printed texts into special enums in base modules


class Character(en.GameObject):
    Characters = list()
    
    def __init__(self, room=None, level=1, health=100, attack=1, strength=1, defence=1):
        Character.Characters.append(self)
        super().__init__(room)
        self.level = level
        self.health = health
        self.attack = attack
        self.strength = strength
        self.defence = defence


#############################################################################################
class Player(Character):
    Players = list()
    
    def __init__(self, name=None, room=None, level=1, health=100, attack=1, strength=1, defence=1):
        Player.Players.append(self)
        super().__init__(room, level, health, attack, strength, defence)
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
            y=[x for x in self.room.items if x.name == item][0]
            print(y)
            # self.inventory.append([x for x in self.room.items if x.name==item][0])
            self.inventory.append(y)
            # self.room.items.remove([x for x in self.room.items if x.name==item][0])
            self.room.items.remove(y)
            print(f"I have picked up {y.name}.")
            if isinstance(y, we.Weapon):
                print(f"It has bonus {y.att_bonus} - consider wielding it.")
                
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
            en.Battle.fight(self, [monster for monster in self.room.monsters if monster.name==other][0])
        
    def wield(self, item):
        if item not in [x.name for x in self.inventory]:
            print("I cannot wield something I dont have.")
            return
        self.wielded_weapon = [x for x in self.inventory if x.name == item][0]
        self.attack += self.wielded_weapon.att_bonus
        self.inventory.remove([x for x in self.inventory if x.name == item][0])
        
    def go(self, direction):
        cil=self.room.neighbours.get(direction)
        if not cil:
            print(f"There is no room in direction of {direction}.")
        else:
            cil.players.append(self)
            self.room.players.remove(self)
            self.room = cil
    
        
#############################################################################################
class Monster(Character):
    Monsters = list()
        
    def __init__(self, name=None, room=None, level=1, health=100, attack=1, strength=1, defence=1):
        Monster.Monsters.append(self)
        super().__init__(room, level, health, attack, strength, defence)
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
