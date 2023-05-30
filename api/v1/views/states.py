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
    """ Retrieves the list of all State objects """
    all_states = storage.all(State).values()
    state_list = []
    for states in all_states:
        state_list.append(states.to_dict())
    return jsonify(state_list)

@app_views.route("/states/<state_id>", strict_slashes=False)
def states_by_id(state_id):
    """ Retrieves a State object """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)

@app_views.route("/states/<state_id>", methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get(State, state_id)
    if state:
        empty_dict = {}
        storage.delete(state)
        storage.save()
        response = make_response(jsonify(empty_dict), 200)
        return response
    else:
        abort(404)

@app_views.route("/states", methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State """
    data = request.get_json()
    if data:
        try:
            json.dumps(data)
        except ValueError:
            return jsonify('Not a JSON'), 400
    if 'name' in data:
        new_state = State().to_dict()
        for key, value in data.items():
            new_state[key] = value
        response = make_response(jsonify(new_state), 201)
        return response
    else:
        return jsonify('Missing name'), 400

@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State """
    state = storage.get(State, state_id)
    if state:
