"""
World module for MUDpy SS13.
This module provides the world state and game object management.
"""

import logging
import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import os

# Set up module logger
logger = logging.getLogger(__name__)

@dataclass
class GameObject:
    """
    Base class for all game objects.
    
    Game objects have an ID, name, description, and components.
    """
    id: str
    name: str
    description: str
    location: Optional[str] = None
    components: Dict[str, Any] = field(default_factory=dict)
    
    def add_component(self, comp_name: str, comp: Any) -> None:
        """
        Add a component to this game object.
        
        Args:
            comp_name (str): The name/type of the component.
            comp (Any): The component instance.
        """
        self.components[comp_name] = comp
        if hasattr(comp, 'owner'):
            comp.owner = self
        logger.debug(f"Added {comp_name} component to {self.id}")
        
    def get_component(self, comp_name: str) -> Optional[Any]:
        """
        Get a component by name.
        
        Args:
            comp_name (str): The name/type of the component.
            
        Returns:
            Optional[Any]: The component if found, None otherwise.
        """
        return self.components.get(comp_name)
    
    def has_component(self, comp_name: str) -> bool:
        """
        Check if this game object has a component.
        
        Args:
            comp_name (str): The name/type of the component.
            
        Returns:
            bool: True if the component exists, False otherwise.
        """
        return comp_name in self.components
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert this game object to a dictionary for serialization.
        
        Returns:
            Dict[str, Any]: Dictionary representation of this object.
        """
        components_dict = {}
        for name, comp in self.components.items():
            if hasattr(comp, 'to_dict'):
                components_dict[name] = comp.to_dict()
            # Skip components that can't be serialized
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'components': components_dict
        }

class World:
    """
    The World class manages all game objects and world state.
    """
    
    def __init__(self, data_dir: str = 'data'):
        """
        Initialize the world.
        
        Args:
            data_dir (str): Directory containing world data files.
        """
        self.data_dir = data_dir
        self.objects: Dict[str, GameObject] = {}
        self.rooms: Dict[str, GameObject] = {}
        self.items: Dict[str, GameObject] = {}
        self.npcs: Dict[str, GameObject] = {}
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        logger.info(f"World initialized with data directory: {data_dir}")
    
    def register(self, obj: GameObject) -> None:
        """
        Register a game object in the world.
        
        Args:
            obj (GameObject): The game object to register.
        """
        self.objects[obj.id] = obj
        
        # Also add to type-specific collections for convenience
        if obj.get_component('room'):
            self.rooms[obj.id] = obj
        elif obj.get_component('npc'):
            self.npcs[obj.id] = obj
        elif obj.get_component('item'):
            self.items[obj.id] = obj
            
        logger.debug(f"Registered object: {obj.id}")
    
    def get_object(self, obj_id: str) -> Optional[GameObject]:
        """
        Get a game object by ID.
        
        Args:
            obj_id (str): The ID of the object.
            
        Returns:
            Optional[GameObject]: The game object if found, None otherwise.
        """
        return self.objects.get(obj_id)
    
    def get_objects_in_location(self, location_id: str) -> List[GameObject]:
        """
        Get all objects in a location.
        
        Args:
            location_id (str): The ID of the location.
            
        Returns:
            List[GameObject]: List of objects in the location.
        """
        return [obj for obj in self.objects.values() if obj.location == location_id]
    
    def load_from_file(self, filename: str) -> int:
        """
        Load game objects from a YAML file.
        
        Args:
            filename (str): The name of the file to load.
            
        Returns:
            int: The number of objects loaded.
        """
        filepath = os.path.join(self.data_dir, filename)
        if not os.path.exists(filepath):
            logger.warning(f"File not found: {filepath}")
            return 0
        
        try:
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
            
            count = 0
            if isinstance(data, list):
                for obj_data in data:
                    obj = GameObject(
                        id=obj_data['id'],
                        name=obj_data['name'],
                        description=obj_data.get('description', ''),
                        location=obj_data.get('location')
                    )
                    
                    # Add components (to be implemented later)
                    # This is a placeholder for the component system
                    if 'components' in obj_data:
                        for comp_name, comp_data in obj_data['components'].items():
                            # In a real implementation, we'd instantiate the appropriate component
                            obj.components[comp_name] = comp_data
                    
                    self.register(obj)
                    count += 1
                
                logger.info(f"Loaded {count} objects from {filepath}")
                return count
            else:
                logger.error(f"Expected a list in {filepath}, got {type(data)}")
                return 0
                
        except Exception as e:
            logger.error(f"Error loading {filepath}: {e}")
            return 0
    
    def save_to_file(self, filename: str) -> bool:
        """
        Save all game objects to a YAML file.
        
        Args:
            filename (str): The name of the file to save to.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        filepath = os.path.join(self.data_dir, filename)
        try:
            # Convert objects to dictionaries
            obj_list = [obj.to_dict() for obj in self.objects.values()]
            
            with open(filepath, 'w') as f:
                yaml.dump(obj_list, f, default_flow_style=False, sort_keys=False)
            
            logger.info(f"Saved {len(obj_list)} objects to {filepath}")
            return True
        
        except Exception as e:
            logger.error(f"Error saving to {filepath}: {e}")
            return False

# Create a global world instance
WORLD = World()

def get_world() -> World:
    """
    Get the global world instance.
    
    Returns:
        World: The global world instance.
    """
    return WORLD