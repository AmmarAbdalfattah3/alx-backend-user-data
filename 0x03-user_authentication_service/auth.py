#!/usr/bin/env python3
"""
Auth module
"""


import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """
    Generates a new UUID and returns its string representation.

    Returns:
        str: A string representation of the generated UUID.
    """
    return str(uuid.uuid4())


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    password_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password


class Auth:
    """
    Auth class to interact with the authentication database.

    Attributes:
        _db (DB): Private instance of the DB class
        used to interact with the database.
    """

    def __init__(self):
        """
        Initializes the Auth class with a new DB instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials.

        Args:
            mail (str): The email of the user.
            password (str): The password provided by the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(
                        password.encode('utf-8'),
                        user.hashed_password
                    ):
                return True
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user with the provided email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID if the user is found and session is created.
                 None if the user is not found.
        """
        try:
            # Find the user by email
            user = self._db.find_user_by(email=email)

            # Generate a new session ID
            session_id = _generate_uuid()

            # Update the user's session_id and commit changes
            self._db.update_user(user.id, session_id=session_id)

            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve a User object based on a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            User: The corresponding User object, or None if no user is found.
        """
        if session_id is None:
            return None

        try:
            # Find the user by the session_id in the database
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            # If no user is found, return None
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a session by setting the user's session_id to None.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        try:
            # Find the user by ID and update the session_id to None
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass
