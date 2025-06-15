"""
Script Manager for MUDpy SS13.
Provides a secure sandbox for executing dynamic in-game scripts.
"""

import logging
import traceback
from typing import Dict, Any, Callable, Optional
import re
from events import publish

logger = logging.getLogger(__name__)

# Dictionary to store registered scripts
SCRIPTS: Dict[str, Dict[str, Any]] = {}


class ScriptSandbox:
    """
    A sandbox for safely executing user-provided Python code.

    This is a placeholder implementation. In a production system, you would use
    a proper sandboxing solution like RestrictedPython or PyPy's sandboxing.
    """

    def __init__(self, owner_id: str):
        """
        Initialize the sandbox.

        Args:
            owner_id (str): The ID of the script owner.
        """
        self.owner_id = owner_id
        self.globals = {
            # Restricted set of built-ins
            "abs": abs,
            "bool": bool,
            "dict": dict,
            "float": float,
            "int": int,
            "len": len,
            "list": list,
            "max": max,
            "min": min,
            "range": range,
            "round": round,
            "sorted": sorted,
            "str": str,
            "sum": sum,
            "tuple": tuple,
            # No access to open, eval, exec, import, etc.
        }

    def add_api(self, name: str, func: Callable) -> None:
        """
        Add an API function to the sandbox.

        Args:
            name (str): The name of the function in the sandbox.
            func (Callable): The function to add.
        """
        self.globals[name] = func

    def execute(
        self, code: str, locals_dict: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute code in the sandbox.

        Args:
            code (str): The code to execute.
            locals_dict (Dict[str, Any], optional): Initial local variables.

        Returns:
            Dict[str, Any]: The resulting local variables.
        """
        if locals_dict is None:
            locals_dict = {}

        # In a real implementation, you would use RestrictedPython here
        # For now, we'll do some very basic security checks

        # Check for dangerous constructs
        dangerous_patterns = [
            r"import\s+",
            r"from\s+.*\s+import",
            r"exec\s*\(",
            r"eval\s*\(",
            r"__[a-zA-Z]+__",  # Dunder methods
            r"globals\s*\(\s*\)",
            r"locals\s*\(\s*\)",
            r"open\s*\(",
            r"file\s*\(",
            r"compile\s*\(",
        ]

        for pattern in dangerous_patterns:
            if re.search(pattern, code):
                logger.warning(f"Dangerous pattern found in script: {pattern}")
                raise ValueError(
                    f"Security violation: {pattern} not allowed in scripts"
                )

        # Execute the code with restricted globals
        try:
            # This is not secure and is just for demonstration purposes
            # In a real implementation, use RestrictedPython
            exec(code, self.globals, locals_dict)
            return locals_dict
        except Exception as e:
            logger.error(f"Error executing script: {str(e)}")
            logger.error(traceback.format_exc())
            raise


def register_script(
    script_id: str, owner_id: str, name: str, description: str, code: str
) -> bool:
    """
    Register a new script.

    Args:
        script_id (str): Unique identifier for this script.
        owner_id (str): The ID of the script owner.
        name (str): Human-readable name for this script.
        description (str): Description of what this script does.
        code (str): The Python code for this script.

    Returns:
        bool: True if the script was registered successfully, False otherwise.
    """
    try:
        # Create a sandbox and validate the script
        sandbox = ScriptSandbox(owner_id)

        # Try executing the script to validate it
        sandbox.execute(code)

        # If we got here, the script is valid
        SCRIPTS[script_id] = {
            "owner_id": owner_id,
            "name": name,
            "description": description,
            "code": code,
            "created_at": None,  # In a real system, you would use datetime.datetime.now()
            "modified_at": None,  # Same as above
        }

        logger.info(f"Registered script {script_id} ({name}) by {owner_id}")
        publish("script_registered", script_id=script_id, owner_id=owner_id, name=name)

        return True

    except Exception as e:
        logger.error(f"Failed to register script {script_id}: {str(e)}")
        return False


def unregister_script(script_id: str, requester_id: str) -> bool:
    """
    Unregister a script.

    Args:
        script_id (str): The ID of the script to unregister.
        requester_id (str): The ID of the entity requesting the unregistration.

    Returns:
        bool: True if the script was unregistered, False otherwise.
    """
    if script_id not in SCRIPTS:
        return False

    script_info = SCRIPTS[script_id]

    # Check if the requester is the owner or an admin
    # In a real system, you would check if requester_id is an admin
    if script_info["owner_id"] != requester_id:
        logger.warning(
            f"Unauthorized attempt to unregister script {script_id} by {requester_id}"
        )
        return False

    del SCRIPTS[script_id]
    logger.info(f"Unregistered script {script_id}")
    publish("script_unregistered", script_id=script_id, requester_id=requester_id)

    return True


def execute_script(script_id: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Execute a registered script.

    Args:
        script_id (str): The ID of the script to execute.
        context (Dict[str, Any]): The context in which to execute the script.

    Returns:
        Optional[Dict[str, Any]]: The resulting locals dictionary, or None if execution failed.
    """
    if script_id not in SCRIPTS:
        logger.warning(f"Attempt to execute non-existent script {script_id}")
        return None

    script_info = SCRIPTS[script_id]

    try:
        sandbox = ScriptSandbox(script_info["owner_id"])
        result = sandbox.execute(script_info["code"], context.copy())
        logger.debug(f"Successfully executed script {script_id}")
        return result

    except Exception as e:
        logger.error(f"Failed to execute script {script_id}: {str(e)}")
        return None


def get_script_info(script_id: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a registered script.

    Args:
        script_id (str): The ID of the script.

    Returns:
        Optional[Dict[str, Any]]: Information about the script, or None if not found.
    """
    return SCRIPTS.get(script_id)


def list_scripts(owner_id: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
    """
    List registered scripts.

    Args:
        owner_id (str, optional): If provided, only list scripts by this owner.

    Returns:
        Dict[str, Dict[str, Any]]: Dictionary of script_id -> script info.
    """
    if owner_id:
        return {
            sid: info for sid, info in SCRIPTS.items() if info["owner_id"] == owner_id
        }
    else:
        return SCRIPTS.copy()


def add_verb_to_object(
    obj_id: str, verb: str, code: str, owner_id: str
) -> Optional[str]:
    """
    Add a custom verb to a game object.

    Args:
        obj_id (str): The ID of the game object.
        verb (str): The name of the verb to add.
        code (str): The Python code for this verb.
        owner_id (str): The ID of the verb owner.

    Returns:
        Optional[str]: The ID of the created script, or None if creation failed.
    """
    # Create a unique script ID
    script_id = f"verb_{obj_id}_{verb}"

    # Register the script
    success = register_script(
        script_id=script_id,
        owner_id=owner_id,
        name=f"Verb '{verb}' for {obj_id}",
        description=f"Custom verb implemented for object {obj_id}",
        code=code,
    )

    if success:
        logger.info(f"Added verb '{verb}' to object {obj_id}")
        publish("verb_added", object_id=obj_id, verb=verb, owner_id=owner_id)
        return script_id
    else:
        return None
