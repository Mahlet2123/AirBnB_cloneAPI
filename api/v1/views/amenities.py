#!/usr/bin/python3
"""
Creating a view for Amenity objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity
import json


@app_views.route("/amenities", strict_slashes=False)
def amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenities = storage.all(Amenity).values()
    amenity_list = []
    for amenity in all_amenities:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Retrieves an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route(
        "/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False
        )
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates an Amenity object
    """
    data = request.get_json()
    if not data:
        return jsonify("Not a JSON"), 400
    if "name" in data:
        new_amenity = Amenity(**data)
        storage.new(new_amenity)
        storage.save()
        dict_ = new_amenity.to_dict()
        return jsonify(dict_), 201
    else:
        return jsonify("Missing name"), 400


@app_views.route(
        "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
        )
def update_amenity(amenity_id):
    """
    Updates an Amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        for key, value in data.items():
            list_ = ["id", "created_at", "updated_at"]
            if key not in list_:
                setattr(amenity, key, value)
        storage.save()
        dict_ = amenity.to_dict()
        response = make_response(jsonify(dict_), 200)
        return response
    else:
        abort(404)
