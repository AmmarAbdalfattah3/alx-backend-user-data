#!/usr/bin/env python3
"""BasicAuth module
"""


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
