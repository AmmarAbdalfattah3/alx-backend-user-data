#!/usr/bin/env python3
"""Auth class
"""


from typing import List, TypeVar
from flask import Request


User = TypeVar('User')


class Auth:
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

    def authorization_header(self, request: Request = None) -> str:
        """Return the authorization header"""
        return None

    def current_user(self, request: Request = None) -> User:
        """Return the current user"""
        return None
