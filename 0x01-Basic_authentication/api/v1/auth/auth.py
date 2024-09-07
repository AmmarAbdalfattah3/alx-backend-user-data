#!/usr/bin/env python3
"""
Auth class for managing API authentication.
This is the template for all authentication systems.
"""


from typing import List, TypeVar, Optional
from flask import request


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
        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize path by removing trailing slashes for comparison
        normalized_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            if normalized_path.startswith(normalized_excluded_path):
                return False

        return True

    def authorization_header(
                self, request=None
            ) -> Optional[str]:
        """
        Retrieves the Authorization header from the request.

        Args:
            request: The Flask request object (optional).

        Returns:
            str: None for now, since no authorization
            header is processed.
        """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(
                self, request: Optional[Request] = None
            ) -> Optional[User]:
        """
        Retrieves the current user from the request.

        Args:
            request: The Flask request object (optional).

        Returns:
            TypeVar('User'): None for now, as no user is identified yet.
        """
        return None
