# generic dependencies
import random

# package specific dependencies
from pekascape import character as ch
from pekascape import environment as en
from pekascape import items as it

#    first instantiate room
w = en.MazeWorld(30, 30)

random_frame = w.random_frame

John = ch.Player(name="John", room=random_frame)
Henry = ch.Monster(name="Henry", room=random_frame, health=3)

John.room

John.see()

for i in range(500):
    ch.Monster(attack=random.randint(10, 50))

for x in range(300):
    # r11.items.append(we.Weapon())
    it.Weapon()

for x in range(100):
    it.Bread()
