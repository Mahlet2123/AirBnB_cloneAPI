#!/usr/bin/python3
"""
Creating a view for User objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User
import json


@app_views.route("/users", strict_slashes=False)
def users():
    """
    Retrieves the list of all User objects
    """
    all_users = storage.all(User).values()
    user_list = []
    for users in all_users:
        user_list.append(users.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", strict_slashes=False)
def users_by_id(user_id):
    """
    Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route(
        "/users/<user_id>", methods=["DELETE"], strict_slashes=False
        )
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if user:
        empty_dict = {}
        storage.delete(user)
        storage.save()
        response = make_response(jsonify(empty_dict), 200)
        return response
    else:
        abort(404)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a User
    """
    data = request.get_json()
    if not data:
        return jsonify('Not a JSON'), 400
    if "email" not in data:
        return jsonify("Missing email"), 400
    if "password" not in data:
        return jsonify("Missing password"), 400
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    dict_ = new_user.to_dict()
    return jsonify(dict_), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User
    """
    user = storage.get(User, user_id)
    if user:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        for key, value in data.items():
            list_ = ["id", "created_at", "updated_at"]
            if key not in list_:
                setattr(user, key, value)
        storage.save()
        dict_ = user.to_dict()
        response = make_response(jsonify(dict_), 200)
        return response
    else:
        abort(404)
