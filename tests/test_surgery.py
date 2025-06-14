import world
from world import GameObject, World
from components.player import PlayerComponent
from components.item import ItemComponent
from systems.surgery import SurgerySystem


def test_surgery_procedure(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w

    surgeon = GameObject(id="surgeon", name="doc", description="")
    s_comp = PlayerComponent(skills={"surgery": 3}, inventory=["scalpel", "suture_kit"])
    surgeon.add_component("player", s_comp)
    w.register(surgeon)

    patient = GameObject(id="patient", name="pat", description="")
    p_comp = PlayerComponent()
    patient.add_component("player", p_comp)
    w.register(patient)

    system = SurgerySystem()
    assert system.start_procedure("surgeon", "patient", "appendectomy") is True
    assert system.perform_step("surgeon", "patient") == "incision"
    assert system.perform_step("surgeon", "patient") == "remove_appendix"
    assert system.perform_step("surgeon", "patient") == "suture"
    assert ("surgeon", "patient") not in system.active
    assert p_comp.body_parts["torso"]["brute"] == 0


def test_diagnostic_scanner(tmp_path):
    w = World(data_dir=str(tmp_path))
    world.WORLD = w

    patient = GameObject(id="patient", name="pat", description="")
    p_comp = PlayerComponent()
    patient.add_component("player", p_comp)
    w.register(patient)
    p_comp.apply_damage("torso", "brute", 5)
    p_comp.contract_disease("flu")

    scanner = GameObject(id="scanner", name="scanner", description="")
    scanner.add_component(
        "item",
        ItemComponent(is_takeable=True, is_usable=True, item_type="diagnostic"),
    )
    w.register(scanner)

    msg = scanner.get_component("item").use("patient")
    assert "torso brute: 5" in msg
    assert "Diseases:" in msg
