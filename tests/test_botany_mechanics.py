import world
from world import GameObject, World
from components.player import PlayerComponent
from systems.botany import BotanySystem, get_botany_system
from commands.botanist import plant_handler, fertilize_handler, analyze_handler


def test_apply_fertilizer():
    system = BotanySystem(growth_rate=0.1, tick_interval=0)
    plant = system.plant_seed("tomato")
    pre_nutrient = plant.nutrient
    pre_yield = plant.yield_amount
    system.apply_fertilizer(plant.plant_id, "ammonia")
    assert plant.nutrient > pre_nutrient
    assert plant.yield_amount > pre_yield


def test_botanist_command_flow(tmp_path):
    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        player = GameObject(id="player_test", name="Tester", description="")
        player.add_component("player", PlayerComponent(role="botanist"))
        world.WORLD.register(player)

        system = get_botany_system()
        system.plants.clear()

        plant_handler("test", "wheat")
        plant_id = next(iter(system.plants))
        fertilize_handler("test", plant_id=plant_id, chemical="nutriment")
        out = analyze_handler("test", plant_id=plant_id)
        assert "growth" in out
    finally:
        world.WORLD = old_world

