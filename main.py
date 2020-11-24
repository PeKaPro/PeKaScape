# generic dependencies
import random

# package specific dependencies
from pekascape import character as ch
from pekascape import environment as en
from pekascape import weapon as we
from pekascape import food as fd

#    first instantiate room
en.MapFrame.make_world(30, 30)
en.MapFrame.get_neighbours()

John = ch.Player(name="John")
Henry = ch.Monster(name="Henry", health=3)

for i in range(500):
    ch.Monster(attack=random.randint(10, 50))

for x in range(300):
    # r11.items.append(we.Weapon())
    we.Weapon()

for x in range(100):
    fd.Bread()


