#!/usr/bin/env python3
"""
Flask App Module
"""


from flask import Flask, jsonify, request
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
    # Get email and password from the form data
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if email or password is missing
    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    # Validate login credentials
    if AUTH.valid_login(email, password):
        # Create a new session and get the session ID
        session_id = AUTH.create_session(email)

        # Create a response with a session_id cookie
        response = make_response(
            jsonify({"email": email, "message": "logged in"})
        )
        response.set_cookie('session_id', session_id)
        return response
    else:
        # If login fails, return 401 Unauthorized
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
