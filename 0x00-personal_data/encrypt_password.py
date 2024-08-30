#!/usr/bin/env python3
"""
This module encrypts the password.
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hash a password with a salt using bcrypt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: The hashed password with a salt.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Check if the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The plaintext password to check.

    Returns:
        bool: True if the password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode(), hashed_password)
