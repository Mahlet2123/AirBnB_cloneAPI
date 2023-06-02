#!/usr/bin/python3
"""
Creating a view for Place objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
import json


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def place(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if city:
        place_list = []
        for place in city.places:
            place_list.append(place.to_dict())
        return jsonify(place_list)
    else:
        abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route(
        "/places/<place_id>", methods=["DELETE"], strict_slashes=False
        )
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
        )
def create_place(city_id):
    """
    Creates a Place
    """
    data = request.get_json()
    if not data:
        return jsonify("Not a JSON"), 400
    if "user_id" not in data:
        return jsonify("Missing user_id"), 400
    if "name" not in data:
        return jsonify("Missing name"), 400
    city = storage.get(City, city_id)
    user = storage.get(User, data["user_id"])
    if city and user:
        data["city_id"] = str(city.id)
        new_place = Place(**data)
        storage.new(new_place)
        storage.save()
        dict_ = new_place.to_dict()
        return jsonify(dict_), 201
    else:
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in keys:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
