#!/usr/bin/python3
""" Creating a view for State objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State

@app_views.route("/states", strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State).values()
    state_list = []
    for states in all_states:
        state_list.append(states.to_dict())
    return jsonify(state_list)
