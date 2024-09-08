#!/usr/bin/env python3
""" Module of Users views
"""


from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route(
            '/api/v1/users', methods=['GET'], strict_slashes=False
        )
def view_all_users() -> str:
    """ GET /api/v1/users
    Return:
      - list of all User objects JSON represented
    """
    if request.current_user is None:
        abort(403)
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route(
            '/api/v1/users/<user_id>', methods=['GET'], strict_slashes=False
        )
def view_one_user(user_id: str = None) -> str:
    """ GET /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
    """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_json())

    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route(
            '/api/v1/users/<user_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_user(user_id: str = None) -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON if the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/api/v1/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """ POST /api/v1/users/
    JSON body:
      - email
      - password
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 400 if can't create the new User
    """
    try:
        rj = request.get_json()
        if rj is None:
            raise ValueError("Wrong format")
        email = rj.get("email")
        password = rj.get("password")
        if not email:
            raise ValueError("email missing")
        if not password:
            raise ValueError("password missing")
        user = User()
        user.email = email
        user.password = password
        user.first_name = rj.get("first_name")
        user.last_name = rj.get("last_name")
        user.save()
        return jsonify(user.to_json()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Can't create User: {e}"}), 400


@app_views.route(
            '/api/v1/users/<user_id>', methods=['PUT'], strict_slashes=False
        )
def update_user(user_id: str = None) -> str:
    """ PUT /api/v1/users/:id
    Path parameter:
      - User ID
    JSON body:
      - last_name (optional)
      - first_name (optional)
    Return:
      - User object JSON represented
      - 404 if the User ID doesn't exist
      - 400 if can't update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    try:
        rj = request.get_json()
        if rj is None:
            raise ValueError("Wrong format")
        if rj.get('first_name') is not None:
            user.first_name = rj.get('first_name')
        if rj.get('last_name') is not None:
            user.last_name = rj.get('last_name')
        user.save()
        return jsonify(user.to_json()), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f"Can't update User: {e}"}), 400
