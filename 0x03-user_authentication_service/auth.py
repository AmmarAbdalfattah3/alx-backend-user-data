#!/usr/bin/env python3
"""
Auth module
"""


import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """
        Hashes the input password using bcrypt with a generated salt.

        Args:
            password (str): The password string to be hashed.

        Returns:
            bytes: The salted hash of the input password.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
