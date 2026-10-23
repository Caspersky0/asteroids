
import random

UPGRADES = {
    "rapid_fire": {
        "name": "Rapid Fire",
        "description": "Shoot 30% faster.",
    },
    "double_shot": {
        "name": "Double Shot",
        "description": "Fire two bullets, but shoot 25% slower.",
    },
    "homing": {
        "name": "Homing Rounds",
        "description": "Bullets steer toward nearby enemies.",
    },
    "heavy_rounds": {
        "name": "Heavy Rounds",
        "description": "Bullets have a bigger collision radius.",
    },
}


def get_random_upgrades():
    return random.sample(list(UPGRADES.keys()), 2)
