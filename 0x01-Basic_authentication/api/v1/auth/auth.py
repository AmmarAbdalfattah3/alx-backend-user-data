#!/usr/bin/env python3
"""
Auth class for managing API authentication.
This is the template for all authentication systems.
"""


from typing import List, TypeVar, Request
from flask import Request


User = TypeVar('User')


class Auth:
    """
    A class to manage API authentication.

    This class defines methods to handle authentication logic
    and will be used as a base for all authentication mechanisms.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check for authentication.
            excluded_paths (List[str]): A list of paths
            that do not require authentication.

        Returns:
            bool: False for now, as authentication is not yet required.
        """
        if path is None:
            return True

        if not excluded_paths or len(excluded_paths) == 0:
            return True

        if not path.endswith('/'):
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request: Request = None) -> str:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object (optional).

        Returns:
            str: None for now, since no authorization header is processed.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request: Request = None) -> User:
        """
        Retrieves the current user from the request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): None for now, as no user is identified yet.
        """
        return None
