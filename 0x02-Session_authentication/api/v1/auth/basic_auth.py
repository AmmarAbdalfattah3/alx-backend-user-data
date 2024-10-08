#!/usr/bin/env python3
"""BasicAuth module
"""

from typing import TypeVar
from models.user import User
import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """
    def extract_base64_authorization_header(
                self, authorization_header: str
            ) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.
        Returns the Base64 part or None if conditions are not met.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
                self, base64_authorization_header: str
            ) -> str:
        """
        Decodes a Base64 string into a UTF-8 string.
        Returns the decoded value or None if an error occurs.
        """
        if base64_authorization_header is None or not isinstance(
                    base64_authorization_header, str
                ):
            return None
        try:
            # Decode the Base64 string and return the UTF-8 decoded value
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
                self, decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        Extracts user email and password from the Base64 decoded string
        """
        if (decoded_base64_authorization_header is None or
                not isinstance(decoded_base64_authorization_header, str) or
                ':' not in decoded_base64_authorization_header):
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
                self, user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password
        """
        if (user_email is None or not isinstance(user_email, str) or
                user_pwd is None or not isinstance(user_pwd, str)):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        """
        if request is None:
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
                    auth_header
                )
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
                    base64_auth_header
                )
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
                    decoded_auth_header
                )
        if user_email is None or user_pwd is None:
            return None

        return self.user_object_from_credentials(user_email, user_pwd)
