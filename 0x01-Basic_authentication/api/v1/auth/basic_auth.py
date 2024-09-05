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
        # Return the part after 'Basic ' (which is the Base64 part)
        return authorization_header[6:]  # Remove the "Basic " prefix
