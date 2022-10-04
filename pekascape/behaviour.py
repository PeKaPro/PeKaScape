import random
import time


class Battle:
    """
    Class defining the battle logic - currently very simple
    """

    @staticmethod
    def fight(attacker, defender):
        if hasattr(attacker, "fight") & hasattr(defender, "fight"):
            # formula
            # low and high of a hits are computed for attacker and defender
            attacker_l = round((defender.defence / attacker.attack), 0)
            attacker_h = round((attacker.attack / defender.defence), 0)
            defender_l = round((attacker.defence / defender.attack), 0)
            defender_h = round((defender.attack / attacker.defence), 0)

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
