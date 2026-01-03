"""
Utility functions for the domain layer.
"""
from uuid import uuid4


def get_uuid():
    """
    Generate a new UUID4.
    
    Returns:
        UUID: A new UUID4 object
    """
    return uuid4()
