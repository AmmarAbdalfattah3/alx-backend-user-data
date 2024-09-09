#!/usr/bin/env python3
"""Module defining session authentication routes for Flask."""


from flask import Blueprint, request, jsonify
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


session_auth_blueprint = Blueprint('session_auth', __name__)

auth = SessionAuth()


@session_auth_blueprint.route('/auth_session/login', methods=['POST'])
def login():
    """
    Handles POST requests to /api/v1/auth_session/login.

    This route authenticates a user by validatin.
    If valid, it creates a session and sets a session cookie.

    Returns:
        - JSON response with user data on successful login.
        - Appropriate error messages for missing field.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate that the email is present
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate that the password is present
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for the user by email
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]  # Assuming search returns a list of users

    # Check if the password is correct
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session ID for the user
    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "could not create session"}), 500

    # Set the session cookie in the response
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
