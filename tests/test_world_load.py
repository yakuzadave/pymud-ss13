import os
import yaml
from world import World
from components import ContainerComponent, AccessControlComponent, RoomComponent, ItemComponent


def test_load_from_file_components(tmp_path):
    data = [
        {
            'id': 'room1',
            'name': 'Test Room',
            'description': 'desc',
            'components': {
                'room': {},
                'access': {'required_level': 2}
            }
        },
        {
            'id': 'belt1',
            'name': 'Tool Belt',
            'description': 'belt',
            'components': {
                'item': {},
                'container': {'capacity': 3}
            }
        }
    ]
    file_path = tmp_path / 'objects.yaml'
    with open(file_path, 'w') as f:
        yaml.safe_dump(data, f)

    w = World(data_dir=str(tmp_path))
    count = w.load_from_file('objects.yaml')
    assert count == 2

    room = w.get_object('room1')
    assert isinstance(room.get_component('room'), RoomComponent)
    assert isinstance(room.get_component('access'), AccessControlComponent)

    belt = w.get_object('belt1')
    assert isinstance(belt.get_component('item'), ItemComponent)
    assert isinstance(belt.get_component('container'), ContainerComponent)
