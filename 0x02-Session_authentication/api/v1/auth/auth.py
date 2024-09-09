#!/usr/bin/env python3
"""Auth class
"""


from typing import List, TypeVar
from flask import request
import os


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

    def authorization_header(self, request=None) -> str:
        """Return the authorization header"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> User:
        """Return the current user"""
        return None

    def session_cookie(self, request=None) -> str:
        """
        Retrieves the session cookie value from the request.

        Returns:
            The value of the cookie named SESSION_NAME or None if not present.
        """
        if request is None:
            return None

        # Retrieve the cookie name from environment variable SESSION_NAME
        cookie_name = os.getenv('SESSION_NAME', '_my_session_id')

        # Return the value of the cookie from the request
        return request.cookies.get(cookie_name, None)
