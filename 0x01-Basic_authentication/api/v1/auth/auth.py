#!/usr/bin/env python3
"""Auth class
"""


from typing import List, TypeVar
from flask import Request


User = TypeVar('User')


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determine if authentication is required for a given path"""
        return False

    def authorization_header(self, request: Request = None) -> str:
        """Return the authorization header"""
        return None

    def current_user(self, request: Request = None) -> User:
        """Return the current user"""
        return None
