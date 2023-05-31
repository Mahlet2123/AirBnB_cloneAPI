#!/usr/bin/python3
"""
Creating a view for State objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
import json


@app_views.route("/states", strict_slashes=False)
def states():
    """
    Retrieves the list of all State objects
    """
    all_states = storage.all(State).values()
    state_list = []
    for states in all_states:
        state_list.append(states.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", strict_slashes=False)
def states_by_id(state_id):
    """
    Retrieves a State object
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route(
        "/states/<state_id>", methods=["DELETE"], strict_slashes=False
        )
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)
    if state:
        empty_dict = {}
        storage.delete(state)
        storage.save()
        response = make_response(jsonify(empty_dict), 200)
        return response
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Creates a State
    """
    data = request.get_json()
    if not data:
        return jsonify('Not a JSON'), 400
    if "name" in data:
        new_state = State(**data)
        storage.new(new_state)
        storage.save()
        dict_ = new_state.to_dict()
        return jsonify(dict_), 201
    else:
        return jsonify("Missing name"), 400


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State
    """
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        for key, value in data.items():
            list_ = ["id", "created_at", "updated_at"]
            if key not in list_:
                setattr(state, key, value)
        storage.save()
        dict_ = state.to_dict()
        response = make_response(jsonify(dict_), 200)
        return response
    else:
        abort(404)
