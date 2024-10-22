import random
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pekascape.element import Character


class BasicBattleEngine:
    """
    Class defining the battle logic - currently very simple
    """

    def __init__(self):
        pass

    @staticmethod
    def _calculate_low_hit(defender_def: int, attacker_attack: int) -> int:
        return int(round((defender_def / attacker_attack), 0))

    @staticmethod
    def _calculate_high_hit(attacker_attack: int, defender_def: int) -> int:
        return int(round((attacker_attack / defender_def), 0))

    @classmethod
    def _get_attack_numbers(cls, attacker: 'Character', defender: 'Character') -> tuple[int, int, int, int]:
        # formula
        # low and high of a hits are computed for attacker and defender
        attacker_l = cls._calculate_low_hit(defender.defence, attacker.attack)
        attacker_h = cls._calculate_high_hit(attacker.attack, defender.defence)
        defender_l = cls._calculate_low_hit(attacker.defence, defender.attack)
        defender_h = cls._calculate_high_hit(defender.attack, attacker.defence)

        if attacker_l == attacker_h:
            attacker_h += 1

        if defender_l == defender_h:
            defender_h += 1

        return attacker_l, attacker_h, defender_l, defender_h

    @classmethod
    def fight(cls, attacker: 'Character', defender: 'Character') -> None:
        from pekascape.element import Character  # pylint: disable=import-outside-toplevel
        # TODO: remove when circular imports are fixed

        if not isinstance(attacker, Character):
            raise TypeError(f"Expected type Character, got {type(attacker)}")

        if not isinstance(defender, Character):
            raise TypeError(f"Expected type Character, got {type(defender)}")

        attacker_l, attacker_h, defender_l, defender_h = cls._get_attack_numbers(attacker, defender)

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
                attacker.die()
                return

        defender.die()
