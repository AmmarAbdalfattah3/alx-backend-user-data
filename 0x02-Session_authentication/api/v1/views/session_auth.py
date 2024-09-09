#!/usr/bin/env python3
"""Session Authentication views"""

from flask import request, jsonify
from models.user import User
from api.v1.auth.session_auth import SessionAuth
import os


auth = SessionAuth()


@app.route('/api/v1/auth_session/login', methods=['POST'])
def login():
    """
    Handles POST requests to /api/v1/auth_session/login
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 404

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    if not session_id:
        return jsonify({"error": "could not create session"}), 500

    response = jsonify(user.to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return response
