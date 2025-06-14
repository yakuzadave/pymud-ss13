import yaml
import world
from world import World
from mudpy_interface import MudpyInterface
from integration import MudpyIntegration


def test_player_loading(tmp_path):
    players_dir = tmp_path / "players"
    players_dir.mkdir()
    player_data = [{
        "id": "player_test",
        "name": "Test Player",
        "description": "tester",
        "components": {
            "player": {
                "inventory": [],
                "stats": {"health": 100.0},
                "access_level": 0,
                "current_location": "start",
                "role": "crew",
                "abilities": []
            }
        }
    }]
    with open(players_dir / "player_test.yaml", "w") as f:
        yaml.safe_dump(player_data, f)

    old_world = world.WORLD
    world.WORLD = World(data_dir=str(tmp_path))
    try:
        MudpyIntegration(MudpyInterface())
        assert "player_test" in world.WORLD.objects
    finally:
        world.WORLD = old_world
