import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

import world
from world import GameObject, World
from components.player import PlayerComponent
from systems.combat import Weapon, Armor, get_combat_system


def test_simple_attack(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w
    p1 = GameObject(id="p1", name="p1", description="")
    p1.add_component("player", PlayerComponent())
    p2 = GameObject(id="p2", name="p2", description="")
    p2.add_component("player", PlayerComponent())
    w.register(p1)
    w.register(p2)

    sys = get_combat_system()
    sys.weapons.clear()
    sys.armors.clear()

    weapon = Weapon(damage=10, weapon_type="melee")
    sys.register_weapon("club", weapon)

    armor = Armor(protection=0.5, coverage="body")
    sys.register_armor("p2", armor)

    sys.attack("p1", "p2", "club")
    defender = w.get_object("p2").get_component("player")
    assert defender.body_parts["torso"]["brute"] > 0
