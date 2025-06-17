"""
Jobs system for MUDpy SS13.
Handles crew roles, permissions, and duties.
"""

import logging
from typing import Dict, List, Any, Optional
from events import subscribe, publish
import world

logger = logging.getLogger(__name__)


class Job:
    """
    Represents a crew job/role in the station.
    """

    def __init__(
        self,
        job_id: str,
        title: str,
        description: str,
        department: str = "general",
        rank: int = 1,
    ) -> None:
        """
        Initialize a job.

        Args:
            job_id (str): Unique identifier for this job.
            title (str): The title of this job.
            description (str): A description of this job's duties.
        """
        self.job_id = job_id
        self.title = title
        self.description = description
        self.department = department
        self.rank = rank
        self.access_levels: List[int] = []
        self.starting_items: List[Dict[str, Any]] = []
        self.spawn_location: Optional[str] = None
        self.abilities: List[str] = []

    def add_access_level(self, level: int) -> None:
        """
        Add an access level to this job.

        Args:
            level (int): The access level to add.
        """
        if level not in self.access_levels:
            self.access_levels.append(level)
            self.access_levels.sort()

    def add_starting_item(
        self, item_id: str, properties: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Add a starting item for this job.

        Args:
            item_id (str): The ID of the item template.
            properties (Dict[str, Any], optional): Additional properties for this item.
        """
        self.starting_items.append({"item_id": item_id, "properties": properties or {}})

    def set_spawn_location(self, location_id: str) -> None:
        """
        Set the spawn location for this job.

        Args:
            location_id (str): The ID of the spawn location.
        """
        self.spawn_location = location_id

    def add_ability(self, ability: str) -> None:
        """
        Add a special ability for this job.

        Args:
            ability (str): The ability to add.
        """
        if ability not in self.abilities:
            self.abilities.append(ability)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this job to a dictionary for serialization.

        Returns:
            Dict[str, Any]: Dictionary representation of this job.
        """
        return {
            "job_id": self.job_id,
            "title": self.title,
            "description": self.description,
            "department": self.department,
            "rank": self.rank,
            "access_levels": self.access_levels,
            "starting_items": self.starting_items,
            "spawn_location": self.spawn_location,
            "abilities": self.abilities,
        }


class JobSystem:
    """
    System that manages jobs and crew assignments.
    """

    def __init__(self):
        """
        Initialize the job system.
        """
        self.jobs: Dict[str, Job] = {}
        self.assigned_jobs: Dict[str, str] = {}  # player_id -> job_id
        self.commanding_officers: Dict[str, str] = {}

        # Register event handlers
        subscribe("player_join", self.on_player_join)
        subscribe("player_quit", self.on_player_quit)

        logger.info("Job system initialized")

    def register_job(self, job: Job) -> None:
        """
        Register a job with the system.

        Args:
            job (Job): The job to register.
        """
        self.jobs[job.job_id] = job
        current = self.commanding_officers.get(job.department)
        if not current or self.jobs[current].rank < job.rank:
            self.commanding_officers[job.department] = job.job_id
        logger.debug(f"Registered job {job.job_id} ({job.title})")

    def assign_job(self, player_id: str, job_id: str) -> Optional[Job]:
        """
        Assign a job to a player.

        Args:
            player_id (str): The ID of the player.
            job_id (str): The ID of the job to assign.

        Returns:
            Optional[Job]: The assigned job, or None if the job doesn't exist.
        """
        if job_id not in self.jobs:
            return None

        job = self.jobs[job_id]
        self.assigned_jobs[player_id] = job_id
        logger.info(f"Assigned job {job_id} ({job.title}) to player {player_id}")
        publish("job_assigned", player_id=player_id, job_id=job_id, title=job.title)

        return job

    def get_player_job(self, player_id: str) -> Optional[Job]:
        """
        Get the job assigned to a player.

        Args:
            player_id (str): The ID of the player.

        Returns:
            Optional[Job]: The player's job, or None if they have no job.
        """
        if player_id not in self.assigned_jobs:
            return None

        job_id = self.assigned_jobs[player_id]
        return self.jobs.get(job_id)

    def get_all_jobs(self) -> List[Job]:
        """
        Get all registered jobs.

        Returns:
            List[Job]: List of all jobs.
        """
        return list(self.jobs.values())

    def setup_player_for_job(self, player_id: str, player_obj_id: str) -> Optional[str]:
        """
        Set up a player with their job's starting items, access, etc.

        Args:
            player_id (str): The ID of the player.
            player_obj_id (str): The ID of the player's game object.

        Returns:
            Optional[str]: A message about the job setup, or None if the player has no job.
        """
        job = self.get_player_job(player_id)
        if not job:
            return None

        world_instance = world.get_world()
        player_obj = world_instance.get_object(player_obj_id)
        if not player_obj:
            logger.error(f"Player object {player_obj_id} not found")
            return None

        player_comp = player_obj.get_component("player")
        if not player_comp:
            logger.error(f"Player component not found on object {player_obj_id}")
            return None

        # Set access level
        if job.access_levels:
            max_access = max(job.access_levels)
            player_comp.access_level = max_access

        # Update the player's role field
        player_comp.role = job.job_id

        # Move to spawn location if specified
        if job.spawn_location:
            player_comp.move_to(job.spawn_location)

        # Give starting items
        from components import IDCardComponent

        for item_spec in job.starting_items:
            item_id = item_spec["item_id"]
            properties = item_spec.get("properties", {})
            item_obj = world_instance.get_object(item_id)

            if item_obj:
                if item_obj.get_component("item") is None:
                    logger.info(
                        f"Item {item_id} missing item component; skipping"
                    )
                else:
                    if (
                        item_obj.get_component("item").item_type == "id_card"
                        and not item_obj.get_component("id_card")
                    ):
                        access = properties.get(
                            "access_level",
                            item_obj.get_component("item").item_properties.get(
                                "access_level", 0
                            ),
                        )
                        item_obj.add_component(
                            "id_card", IDCardComponent(access_level=access)
                        )
                player_comp.add_to_inventory(item_id)
            else:
                logger.info(
                    f"Would add {item_id} to player {player_id}'s inventory"
                )

        message = f"You have been assigned the role of {job.title}. {job.description}"
        return message

    def get_players_by_job(self, job_id: str) -> List[str]:
        """
        Get all players assigned to a specific job.

        Args:
            job_id (str): The ID of the job.

        Returns:
            List[str]: List of player IDs with this job.
        """
        return [pid for pid, jid in self.assigned_jobs.items() if jid == job_id]

    def has_access(self, player_id: str, required_level: int) -> bool:
        """
        Check if a player has access to a specific security level.

        Args:
            player_id (str): The ID of the player.
            required_level (int): The required access level.

        Returns:
            bool: True if the player has access, False otherwise.
        """
        job = self.get_player_job(player_id)
        if not job:
            return False

        return any(level >= required_level for level in job.access_levels)

    def get_commanding_officer(self, department: str) -> Optional[Job]:
        job_id = self.commanding_officers.get(department)
        if job_id:
            return self.jobs.get(job_id)
        return None

    def reset_assignments(self) -> None:
        """
        Reset all job assignments.
        This might be used when starting a new game session.
        """
        old_assignments = self.assigned_jobs.copy()
        self.assigned_jobs.clear()
        logger.info("Reset all job assignments")
        publish("job_assignments_reset", old_assignments=old_assignments)

    def on_player_join(self, player_id: str) -> None:
        """
        Handle a player joining the game.
        In a real game, you might assign a default job or prompt for selection.

        Args:
            player_id (str): The ID of the joining player.
        """
        # For now, just log the event
        logger.info(f"Player {player_id} joined, no job assigned yet")

    def on_player_quit(self, player_id: str) -> None:
        """
        Handle a player quitting the game.

        Args:
            player_id (str): The ID of the quitting player.
        """
        if player_id in self.assigned_jobs:
            job_id = self.assigned_jobs[player_id]
            del self.assigned_jobs[player_id]
            logger.info(f"Player {player_id} quit, removed job assignment {job_id}")


# Create standard SS13 jobs
def create_standard_jobs() -> Dict[str, Job]:
    """
    Create standard SS13 job roles.

    Returns:
        Dict[str, Job]: Dictionary of job_id -> Job objects.
    """
    jobs = {}

    # Captain
    captain = Job(
        "captain",
        "Captain",
        "You are in command of the station and its crew.",
        "command",
        rank=90,
    )
    captain.add_access_level(100)  # All access
    captain.add_starting_item("captain_id_card", {"access_level": 100})
    captain.add_starting_item(
        "captain_headset",
        {
            "channels": [
                "command",
                "security",
                "engineering",
                "medical",
                "science",
                "supply",
            ]
        },
    )
    captain.add_starting_item("captain_uniform")
    captain.add_starting_item("captain_laser")
    captain.set_spawn_location("bridge")
    jobs[captain.job_id] = captain

    # Security Officer
    security = Job(
        "security",
        "Security Officer",
        "Maintain order and protect the crew.",
        "security",
        rank=50,
    )
    security.add_access_level(30)  # Security access
    security.add_starting_item("security_id_card", {"access_level": 30})
    security.add_starting_item("security_headset", {"channels": ["security"]})
    security.add_starting_item("security_uniform")
    security.add_starting_item("stunbaton")
    security.set_spawn_location("security")
    jobs[security.job_id] = security

    # Engineer
    engineer = Job(
        "engineer",
        "Station Engineer",
        "Keep the station's power and life support systems running.",
        "engineering",
        rank=50,
    )
    engineer.add_access_level(40)  # Engineering access
    engineer.add_starting_item("engineering_id_card", {"access_level": 40})
    engineer.add_starting_item("engineering_headset", {"channels": ["engineering"]})
    engineer.add_starting_item("engineering_uniform")
    engineer.add_starting_item("toolbox")
    engineer.set_spawn_location("engineering")
    jobs[engineer.job_id] = engineer

    # Medical Doctor
    doctor = Job(
        "doctor",
        "Medical Doctor",
        "Treat injuries and save lives.",
        "medical",
        rank=50,
    )
    doctor.add_access_level(50)  # Medical access
    doctor.add_starting_item("medical_id_card", {"access_level": 50})
    doctor.add_starting_item("medical_headset", {"channels": ["medical"]})
    doctor.add_starting_item("medical_uniform")
    doctor.add_starting_item("first_aid_kit")
    doctor.set_spawn_location("medbay")
    jobs[doctor.job_id] = doctor

    # Scientist
    scientist = Job(
        "scientist",
        "Scientist",
        "Research new technologies and study anomalies.",
        "science",
        rank=50,
    )
    scientist.add_access_level(60)  # Science access
    scientist.add_starting_item("science_id_card", {"access_level": 60})
    scientist.add_starting_item("science_headset", {"channels": ["science"]})
    scientist.add_starting_item("science_uniform")
    scientist.add_starting_item("science_scanner")
    scientist.set_spawn_location("research")
    jobs[scientist.job_id] = scientist

    # Chemist
    chemist = Job(
        "chemist",
        "Chemist",
        "Create new compounds and manage reagents for the station.",
        "science",
        rank=40,
    )
    chemist.add_access_level(60)  # Science access
    chemist.add_starting_item("science_id_card", {"access_level": 60})
    chemist.add_starting_item("beaker")
    chemist.add_starting_item("chemical_a")
    chemist.add_starting_item("chemical_b")
    chemist.set_spawn_location("science_lab")
    jobs[chemist.job_id] = chemist

    # Cargo Technician
    cargo = Job(
        "cargo",
        "Cargo Technician",
        "Order and deliver supplies to the station.",
        "supply",
        rank=40,
    )
    cargo.add_access_level(70)  # Cargo access
    cargo.add_starting_item("cargo_id_card", {"access_level": 70})
    cargo.add_starting_item("cargo_headset", {"channels": ["supply"]})
    cargo.add_starting_item("cargo_uniform")
    cargo.set_spawn_location("cargo")
    jobs[cargo.job_id] = cargo

    # Janitor
    janitor = Job(
        "janitor",
        "Janitor",
        "Keep the station clean and tidy.",
        "service",
        rank=20,
    )
    janitor.add_access_level(10)  # Basic access
    janitor.add_starting_item("janitor_id_card", {"access_level": 10})
    janitor.add_starting_item("janitor_headset", {"channels": ["service"]})
    janitor.add_starting_item("janitor_uniform")
    janitor.add_starting_item("mop")
    janitor.add_starting_item("bucket")
    janitor.set_spawn_location("janitorial")
    jobs[janitor.job_id] = janitor

    # Chef
    chef = Job(
        "chef",
        "Chef",
        "Prepare meals for the crew.",
        "service",
        rank=20,
    )
    chef.add_access_level(10)  # Basic access
    chef.add_starting_item("chef_id_card", {"access_level": 10})
    chef.add_starting_item("chef_headset", {"channels": ["service"]})
    chef.add_starting_item("chef_uniform")
    chef.add_starting_item("kitchen_knife")
    chef.set_spawn_location("kitchen")
    jobs[chef.job_id] = chef

    # Bartender
    bartender = Job(
        "bartender",
        "Bartender",
        "Serve drinks and keep the bar orderly.",
        "service",
        rank=20,
    )
    bartender.add_access_level(10)
    bartender.add_starting_item("bartender_id_card", {"access_level": 10})
    bartender.add_starting_item("service_headset", {"channels": ["service"]})
    bartender.add_starting_item("shaker")
    bartender.set_spawn_location("bar")
    jobs[bartender.job_id] = bartender

    # Assistant
    assistant = Job(
        "assistant",
        "Assistant",
        "Learn the ropes and help out where needed.",
        "service",
        rank=10,
    )
    assistant.add_access_level(10)  # Basic access
    assistant.add_starting_item("assistant_id_card", {"access_level": 10})
    assistant.add_starting_item("assistant_headset", {"channels": ["common"]})
    assistant.add_starting_item("assistant_uniform")
    assistant.set_spawn_location("arrival")
    jobs[assistant.job_id] = assistant

    # Traitor - antagonist role
    traitor = Job(
        "traitor",
        "Traitor",
        "Undermine the station and complete covert objectives.",
        "antagonist",
        rank=30,
    )
    traitor.add_access_level(20)
    traitor.add_starting_item("traitor_kit")
    traitor.set_spawn_location("arrival")
    traitor.add_ability("sabotage")
    jobs[traitor.job_id] = traitor

    # Station AI
    ai = Job(
        "ai",
        "Station AI",
        "Oversee station operations and assist the crew.",
        "command",
        rank=85,
    )
    ai.add_access_level(100)
    ai.set_spawn_location("core")
    ai.add_ability("monitor")
    jobs[ai.job_id] = ai

    # Cyborg
    cyborg = Job(
        "cyborg",
        "Cyborg",
        "Robotic assistant with specialized modules.",
        "engineering",
        rank=40,
    )
    cyborg.add_access_level(60)
    cyborg.set_spawn_location("robotics")
    cyborg.add_ability("interface")
    jobs[cyborg.job_id] = cyborg

    return jobs


# Create a global job system instance
JOB_SYSTEM = JobSystem()

# Add standard jobs to the system
for job_id, job in create_standard_jobs().items():
    JOB_SYSTEM.register_job(job)


def get_job_system() -> JobSystem:
    """
    Get the global job system instance.

    Returns:
        JobSystem: The global job system instance.
    """
    return JOB_SYSTEM
