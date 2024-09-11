#!/usr/bin/env python3
"""
Auth module
"""


from db import DB
from user import User
import bcrypt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    import bcrypt

    def _hash_password(password: str) -> bytes:
        """Hash a password using bcrypt

        Args:
            password (str): The password to hash

        Returns:
            bytes: The salted hash of the password
        """
        # Convert the password string to bytes
        password_bytes = password.encode('utf-8')

        # Generate a salted hash using bcrypt
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

        return hashed_password
