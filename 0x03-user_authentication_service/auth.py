#!/usr/bin/env python3
"""Auth module
"""

from db import DB
from user import User
from bcrypt import hashpw, gensalt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """
        Initialize the Auth instance with a DB instance.
        """
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """
        Hashes the input password using bcrypt with a generated salt.

        Args:
            password (str): The password string to be hashed.

        Returns:
            bytes: The salted hash of the input password.
        """
        password_bytes = password.encode('utf-8')

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)

        return hashed_password

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with the provided email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password.decode('utf-8'))
            return user
