import character as ch
import environment as en
import weapon as we
import random

if __name__=="__main__":
#    first instantiate room
    en.MapFrame.MakeWorld(30,30)
    en.MapFrame.GetNeighbours()
    
    John = ch.Player(name="John")
    Henry = ch.Monster(name="Henry",health=3)
    
    for i in range(500):
        ch.Monster(attack=random.randint(10,50))
    
    for x in range(300):
        #r11.items.append(we.Weapon())
        we.Weapon()
#    while True:
        