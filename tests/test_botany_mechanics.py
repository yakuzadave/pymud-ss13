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


def test_cross_pollination_grafting_autogrow():
    system = BotanySystem(growth_rate=0.1, tick_interval=0, cross_poll_chance=1.0)
    plant_a = system.plant_seed("tomato")
    plant_b = system.plant_seed("wheat")
    plant_a.traits.add("glow")
    system.cross_pollination = True
    system.start()
    system.update()
    assert "glow" in plant_b.traits
    system.graft(plant_b.plant_id, plant_a.plant_id)
    assert plant_a.traits.issubset(plant_b.traits)
    system.toggle_autogrow(plant_a.plant_id)
    nutrient_before = plant_a.nutrient
    system.update()
    assert plant_a.nutrient > nutrient_before

