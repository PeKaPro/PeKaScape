# generic dependencies
import random

# package specific dependencies
from pekascape import character as ch
from pekascape import environment as en
from pekascape import items as it

#    first instantiate room
w = en.MazeMap(30, 30)
w.random_frame
random_frame = w.random_frame

John = ch.Player(name="John", room=random_frame)
Henry = ch.Monster(room=random_frame, health=3)

John.room

John.see()

for i in range(500):
    ch.Monster(attack=random.randint(10, 50), room=w.random_frame)

for x in range(300):
    it.WeaponFactory.create_random_weapon(room=w.random_frame)

for x in range(100):
    it.Bread(room=w.random_frame)
