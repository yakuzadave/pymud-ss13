"""
Events system for MUDpy SS13.
This module provides a simple publish-subscribe event system with support for both synchronous
and asynchronous event handlers.
"""

import asyncio
import inspect
import logging
from typing import Callable, Dict, List, Any, Union, Coroutine

# Set up module logger
logger = logging.getLogger(__name__)

# Type for event handlers (can be sync or async)
EventHandler = Union[Callable[..., Any], Callable[..., Coroutine[Any, Any, Any]]]

# Event subscribers registry
# Maps event_name -> list of callback functions
SUBSCRIBERS: Dict[str, List[EventHandler]] = {}

def subscribe(event_name: str, callback: EventHandler) -> None:
    """
    Subscribe a callback function to an event.
    
    Args:
        event_name (str): The name of the event to subscribe to.
        callback (EventHandler): The function to call when the event is published.
            This can be a synchronous or asynchronous function.
    """
    if event_name not in SUBSCRIBERS:
        SUBSCRIBERS[event_name] = []
    
    if callback not in SUBSCRIBERS[event_name]:
        SUBSCRIBERS[event_name].append(callback)
        logger.debug(f"Added subscriber to '{event_name}' event: {callback.__name__}")

def unsubscribe(event_name: str, callback: EventHandler) -> bool:
    """
    Unsubscribe a callback function from an event.
    
    Args:
        event_name (str): The name of the event to unsubscribe from.
        callback (EventHandler): The function to unsubscribe.
        
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
    
    This function calls all subscribers synchronously. For asynchronous
    subscribers, it creates a task but does not await them.
    
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
            # Check if the callback is async
            if inspect.iscoroutinefunction(callback):
                # Create a task for the async callback but don't wait for it
                asyncio.create_task(callback(**kwargs))
            else:
                # Call synchronous callback directly
                callback(**kwargs)
        except Exception as e:
            logger.error(f"Error in subscriber callback for '{event_name}': {e}")
    
    return subscriber_count

async def publish_async(event_name: str, **kwargs: Any) -> int:
    """
    Publish an event to all subscribers and await async callbacks.
    
    This function awaits all async subscribers and calls sync subscribers.
    
    Args:
        event_name (str): The name of the event to publish.
        **kwargs: Data to pass to the subscriber functions.
        
    Returns:
        int: The number of subscribers notified.
    """
    if event_name not in SUBSCRIBERS:
        return 0
    
    subscriber_count = len(SUBSCRIBERS[event_name])
    logger.debug(f"Publishing '{event_name}' event asynchronously to {subscriber_count} subscribers")
    
    tasks = []
    
    for callback in SUBSCRIBERS[event_name]:
        try:
            # Check if the callback is async
            if inspect.iscoroutinefunction(callback):
                # Create a task for the async callback
                task = asyncio.create_task(callback(**kwargs))
                tasks.append(task)
            else:
                # Call synchronous callback directly
                callback(**kwargs)
        except Exception as e:
            logger.error(f"Error in subscriber callback for '{event_name}': {e}")
    
    # Wait for all async tasks to complete
    if tasks:
        await asyncio.gather(*tasks, return_exceptions=True)
    
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
