#!/usr/bin/env python3
"""
Flask App Module
"""


from flask import Flask, jsonify, request, redirect, abort
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """Handle GET requests to the root URL ("/")
       and return a JSON response
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    POST /users route to register a user with email and password.
    If the user is already registered, returns a 400 status code.

    Returns:
        JSON response: Either a success or error message.
    """
    # Get email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Attempt to register the user
        user = AUTH.register_user(email, password)
        # Return success response
        return jsonify(
                    {"email": user.email, "message": "user created"}
                ), 200
    except ValueError:
        # If user already exists, return an error response
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """
    POST /sessions route to log in a user.
    Sets a session ID cookie if login is successful.
    Returns a JSON response indicating the login status.

    Returns:
        JSON response: Either a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400, description="Missing email or password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({
            "email": email,
            "message": "logged in"
        })
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401, description="Invalid login credentials")


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /sessions route to log out a user.
    The request is expected to contain the session ID as a cookie.

    If the session ID is valid, the session is destroyed,
    and the user is redirected.

    If the session ID is invalid or user does not exist,
    respond with a 403 status.

    Returns:
        Flask Response: Redirects to the homepage or returns a 403 error.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """
    GET /profile route to retrieve the profile
    information of a logged-in user.
    The request is expected to contain a session_id cookie.

    If the session ID is valid and the user exists, respond
    with their email.
    If the session ID is invalid or the user does not exist,
    respond with a 403 status.

    Returns:
        JSON response with the user's email or a 403 error.
    """
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """
    POST /reset_password route to generate a reset password token.
    The request must contain form data with the 'email' field.

    Returns:
        JSON response: Either a 403 error if email is not registered
        or a success response with the reset token.
    """
    email = request.form.get('email')

    if not email:
        abort(400, description="Missing email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403, description="Email not registered")

    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """
    PUT /reset_password route to update a user's password.

    The request is expected to contain the following form data:
        - email: The user's email
        - reset_token: The reset token to validate the user
        - new_password: The new password for the user

    Returns:
        A JSON response indicating success or failure.
    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(400, description="Missing email, reset_token, or new_password")

    try:
        AUTH.update_password(reset_token, new_password)

        return jsonify({
            "email": email,
            "message": "Password updated"
        }), 200
    except ValueError:
        abort(403, description="Invalid reset token")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
