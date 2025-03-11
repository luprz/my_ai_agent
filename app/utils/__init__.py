"""Utils module for common helper functions.

This module provides utility functions and common operations
that can be used across different parts of the application.
"""

from typing import Any, Dict, List, Optional, TypeVar, Union

T = TypeVar('T')

def safe_get(obj: Dict[str, Any], key: str, default: Optional[T] = None) -> Optional[T]:
    """Safely get a value from a dictionary.

    Args:
        obj: The dictionary to get the value from
        key: The key to look up
        default: The default value to return if the key is not found

    Returns:
        The value if found, otherwise the default value
    """
    try:
        return obj.get(key, default)
    except (AttributeError, KeyError):
        return default

def flatten_list(lst: List[List[Any]]) -> List[Any]:
    """Flatten a list of lists into a single list.

    Args:
        lst: The list of lists to flatten

    Returns:
        A flattened list
    """
    return [item for sublist in lst for item in sublist]

def ensure_list(value: Union[T, List[T]]) -> List[T]:
    """Ensure a value is a list.

    Args:
        value: The value to convert to a list if it isn't already

    Returns:
        A list containing the value if it wasn't a list, otherwise the original list
    """
    if isinstance(value, list):
        return value
    return [value]