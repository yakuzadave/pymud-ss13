"""
Events system for MUDpy SS13.
This module provides a simple publish-subscribe event system.
"""

import logging
from typing import Callable, Dict, List, Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Event subscribers registry
# Maps event_name -> list of callback functions
SUBSCRIBERS: Dict[str, List[Callable]] = {}

def subscribe(event_name: str, callback: Callable) -> None:
    """
    Subscribe a callback function to an event.
    
    Args:
        event_name (str): The name of the event to subscribe to.
        callback (Callable): The function to call when the event is published.
    """
    if event_name not in SUBSCRIBERS:
        SUBSCRIBERS[event_name] = []
    
    if callback not in SUBSCRIBERS[event_name]:
        SUBSCRIBERS[event_name].append(callback)
        logger.debug(f"Added subscriber to '{event_name}' event: {callback.__name__}")

def unsubscribe(event_name: str, callback: Callable) -> bool:
    """
    Unsubscribe a callback function from an event.
    
    Args:
        event_name (str): The name of the event to unsubscribe from.
        callback (Callable): The function to unsubscribe.
        
    Returns:
        bool: True if successfully unsubscribed, False otherwise.
    """
    if event_name in SUBSCRIBERS and callback in SUBSCRIBERS[event_name]:
        SUBSCRIBERS[event_name].remove(callback)
        logger.debug(f"Removed subscriber from '{event_name}' event: {callback.__name__}")
        return True
    return False

def publish(event_name: str, **kwargs: Any) -> int:
    """
    Publish an event to all subscribers.
    
    Args:
        event_name (str): The name of the event to publish.
        **kwargs: Data to pass to the subscriber functions.
        
    Returns:
        int: The number of subscribers notified.
    """
    if event_name not in SUBSCRIBERS:
        return 0
    
    subscriber_count = len(SUBSCRIBERS[event_name])
    logger.debug(f"Publishing '{event_name}' event to {subscriber_count} subscribers")
    
    for callback in SUBSCRIBERS[event_name]:
        try:
            callback(**kwargs)
        except Exception as e:
            logger.error(f"Error in subscriber callback for '{event_name}': {e}")
    
    return subscriber_count

def get_event_names() -> List[str]:
    """
    Get a list of all registered event names.
    
    Returns:
        List[str]: List of event names with active subscribers.
    """
    return list(SUBSCRIBERS.keys())

def get_subscriber_count(event_name: str) -> int:
    """
    Get the number of subscribers for an event.
    
    Args:
        event_name (str): The name of the event.
        
    Returns:
        int: The number of subscribers.
    """
    return len(SUBSCRIBERS.get(event_name, []))