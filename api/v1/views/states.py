#!/usr/bin/python3
"""A view API for state"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Get all states from storage"""
    all_states = storage.all(State)
    json_format = []
    for state in all_states.values():
        json_format.append(state.to_dict())
    return jsonify(json_format)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states_withId(state_id):
    """Get state with a provided ID"""
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    else:
        return jsonify(the_state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state object if found"""
    the_state = storage.get(State, state_id)
    if the_state is None:
        abort(404)
    else:
        storage.delete(the_state)
        storage.save()
        return {}, 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a state"""
    http_body_request = request.get_json(silent=True)
    if http_body_request is None:
        return "Not a JSON\n", 400
    elif "name" not in http_body_request:
        return "Missing name\n", 400
    else:
        new_state = State(name=http_body_request["name"])
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a given state"""
    the_state = storage.get(State, state_id)
    ignore_keys_list = ["id", "created_at", "updated_at"]
    if the_state is None:
        abort(404)
    else:
        http_body_request = request.get_json(silent=True)
        if http_body_request is None:
            return "Not a JSON\n", 400
        else:
            for key, value in http_body_request.items():
                if key not in ignore_keys_list:
                    setattr(the_state, key, value)
        storage.save()
        return jsonify(the_state.to_dict()), 200
