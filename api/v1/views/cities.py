#!/usr/bin/python3
"""
Creating a view for City objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def city(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if state:
        city_list = []
        for city in state.cities:
            city_list.append(city.to_dict())
        return jsonify(city_list)
    else:
        abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieves a City object.
    """
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
        )
def create_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if state:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        if "name" in data:
            data["state_id"] = str(state.id)
            new_city = City(**data)
            storage.new(new_city)
            storage.save()
            dict_ = new_city.to_dict()
            return jsonify(dict_), 201
        else:
            return jsonify("Missing name"), 400
    else:
        abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if city:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        keys = ["id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in keys:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    else:
        abort(404)
