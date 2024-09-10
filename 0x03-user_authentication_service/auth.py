#!/usr/bin/env python3
"""Auth module
"""

import bcrypt


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
