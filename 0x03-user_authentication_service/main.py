#!/usr/bin/env python3
"""Main module
"""


import requests

BASE_URL = "http://localhost:5000"


# Function to register a new user
def register_user(email: str, password: str) -> None:
    response = requests.post(
                f"{BASE_URL}/users",
                data={'email': email, 'password': password}
            )
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}
    print("register_user: OK")


# Function to try login with wrong password
def log_in_wrong_password(email: str, password: str) -> None:
    response = requests.post(
                f"{BASE_URL}/sessions",
                data={'email': email, 'password': password}
            )
    assert response.status_code == 401
    print("log_in_wrong_password: OK")


# Function to login with correct email and password
def log_in(email: str, password: str) -> str:
    response = requests.post(
                f"{BASE_URL}/sessions",
                data={'email': email, 'password': password}
            )
    assert response.status_code == 200
    assert "session_id" in response.cookies
    print("log_in: OK")
    return response.cookies.get('session_id')


# Function to check profile when not logged in
def profile_unlogged() -> None:
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403
    print("profile_unlogged: OK")


# Function to check profile when logged in
def profile_logged(session_id: str) -> None:
    cookies = {'session_id': session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200
    print("profile_logged: OK")


# Function to log out
def log_out(session_id: str) -> None:
    cookies = {'session_id': session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200
    print("log_out: OK")


# Function to get a reset password token
def reset_password_token(email: str) -> str:
    response = requests.post(
                f"{BASE_URL}/reset_password",
                data={'email': email}
            )
    assert response.status_code == 200
    reset_token = response.json().get('reset_token')
    assert reset_token is not None
    print("reset_password_token: OK")
    return reset_token


# Function to update password using the reset token
def update_password(
            email: str, reset_token: str, new_password: str
        ) -> None:
    response = requests.put(f"{BASE_URL}/reset_password", data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}
    print("update_password: OK")


# Test the full flow
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
