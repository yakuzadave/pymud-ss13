from engine import register
from systems.research import get_research_system


@register("research")
def research_handler(client_id: str, tech_id: str, *args, **kwargs):
    """Attempt to research a technology for the science department."""
    system = get_research_system()
    dept = "science"  # Placeholder: in game this would be determined from player role
    if system.research(dept, tech_id):
        return f"Technology {tech_id} researched."
    return "Research failed." 


@register("prototype")
def prototype_handler(client_id: str, proto_id: str, *materials):
    """Build a prototype if requirements are met."""
    system = get_research_system()
    dept = "science"
    equipment = ["workbench"]
    if system.build_prototype(dept, proto_id, list(materials), equipment):
        return f"Prototype {proto_id} constructed."
    return "Prototype construction failed."
