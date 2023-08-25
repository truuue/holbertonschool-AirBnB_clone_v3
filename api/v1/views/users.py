#!/usr/bin/python3
"""A view API for users"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """Get all users"""
    users = storage.all(User)
    json_format = []
    for user in users.values():
        json_format.append(user.to_dict())
    return jsonify(json_format)


@app_views.route("/users/<user_id>", methods=["GET"],
                 strict_slashes=False)
def get_user_withId(user_id):
    """Get user with a provided ID"""
    the_user = storage.get(User, user_id)
    if the_user is None:
        abort(404)
    else:
        return jsonify(the_user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object if found"""
    the_user = storage.get(User, user_id)
    if the_user is None:
        abort(404)
    else:
        storage.delete(the_user)
        storage.save()
        return {}, 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a user"""
    http_body_request = request.get_json(silent=True)
    if http_body_request is None:
        return "Not a JSON\n", 400
    elif "email" not in http_body_request:
        return "Missing email\n", 400
    elif "password" not in http_body_request:
        return "Missing password\n", 400
    else:
        new_user = User(email=http_body_request["email"],
                        password=http_body_request["password"])
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a given user"""
    the_user = storage.get(User, user_id)
    ignore_keys_list = ["id", "created_at", "updated_at", "email"]
    if the_user is None:
        abort(404)
    else:
        http_body_request = request.get_json(silent=True)
        if http_body_request is None:
            return "Not a JSON\n", 400
        else:
            for key, value in http_body_request.items():
                if key not in ignore_keys_list:
                    setattr(the_user, key, value)
        storage.save()
        return jsonify(the_user.to_dict()), 200
