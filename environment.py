import random
import time


class MapFrame:
    
    MapFrames = list()
    MapFramesCoors = dict()
    """This is the basic world element 
    to incorporate the player-environment interaction"""
    def __init__(self, x, y):
        
        MapFrame.MapFrames.append(self)
        MapFrame.MapFramesCoors[(x, y)] = self
        
        self.x = x 
        self.y = y 
        
        self.items = list()
        self.monsters = list()
        self.players = list()
        self.neighbours = dict()
        
    def set_neighbours(self,x=None,y=None,direction=None):
        if direction is None:
            self.neighbours["north"]=MapFrame.MapFramesCoors.get((self.x,self.y+1))
            self.neighbours["south"]=MapFrame.MapFramesCoors.get((self.x,self.y-1))
            self.neighbours["east"]=MapFrame.MapFramesCoors.get((self.x+1,self.y))
            self.neighbours["west"]=MapFrame.MapFramesCoors.get((self.x-1,self.y))
        else:
            self.neighbours[direction]=MapFrame.MapFramesCoors.get((x,y))
        
    @staticmethod
    def get_neighbours():
        for mapframe in MapFrame.MapFrames:
            mapframe.set_neighbours()
    
    @staticmethod        
    def make_world(x, y):
        for i in range(x):
            for j in range(y):
                MapFrame(i, j)


class GameObject:
    game_objects = list()
    
    def __init__(self, room = None):
        if not MapFrame.MapFrames:
            MapFrame(1, 1)
            """This is to prevent creation of GameObjects 
            before at least one MapFrame was instantiated."""
        self.game_objects.append(self)
        self.room = room if room is not None else random.choice(MapFrame.MapFrames)


#############################################################################################
class Battle:

    @staticmethod
    def fight(attacker, defender):
        if hasattr(attacker, "fight") & hasattr(defender, "fight"):
            # formula
            # low and high of a hits are computed for attacker and defender
            attacker_l = round((defender.defence / attacker.attack ),0)
            attacker_h = round((attacker.attack / defender.defence ),0)
            
            defender_l = round((attacker.defence / defender.attack ),0)
            defender_h = round((defender.attack / attacker.defence ),0)
            
            while attacker.health > 0 and defender.health > 0:
                attacker_hit = random.randint(attacker_l, attacker_h)
                defender.health -= attacker_hit
                print(f"{defender.name} was hit and lost {attacker_hit} health.")
                
                time.sleep(0.4)
                
                defender_hit = random.randint(defender_l, defender_h)
                attacker.health -= defender_hit
                print(f"{attacker.name} was hit and lost {defender_hit} health.\n")
                
                time.sleep(0.4)

                if attacker.health < 0:
                    print('Too bad, you died...')
                    attacker.alive = 0
            
        else: 
            print("Either one of attacker of defender is not a type for combat.")
