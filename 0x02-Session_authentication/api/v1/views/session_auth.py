#!/usr/bin/env python3
"""Session Authentication views"""


from flask import Blueprint, request, jsonify
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


# Create a Blueprint for the session auth views
session_auth_blueprint = Blueprint('session_auth', __name__)

# Initialize SessionAuth instance
auth = SessionAuth()


@session_auth_blueprint.route('/auth_session/login', methods=['POST'])
def login():
    """
    Handles POST requests to /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    # Check for email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Check for password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve user based on email
    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    # Verify password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create session
    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "could not create session"}), 500

    # Prepare response
    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
