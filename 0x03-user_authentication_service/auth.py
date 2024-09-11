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
        """Hashes a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the provided email and password.

        Args:
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the email already exists.
        """
        try:
            # Check if the user already exists
            self._db.find_user_by(email=email)
            # If the above does not raise an exception, user already exists
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # User does not exist, proceed with registration
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user
