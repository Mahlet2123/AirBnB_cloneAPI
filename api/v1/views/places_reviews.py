#!/usr/bin/python3
"""
Creating a view for Review objects that handles all
default RESTFul API actions
"""


from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
import json


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def review(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place:
        review_list = []
        for review in place.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def review_by_id(review_id):
    """
    Retrieves a Review object.
    """
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route(
        "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
        )
def delete_review(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route(
        "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
        )
def create_review(place_id):
    """
    Creates a Review
    """
    data = request.get_json()
    if not data:
        return jsonify("Not a JSON"), 400
    if "user_id" not in data:
        return jsonify("Missing user_id"), 400
    if "text" not in data:
        return jsonify("Missing text"), 400

    place = storage.get(Place, place_id)
    user = storage.get(User, data["user_id"])
    if place and user:
        data["place_id"] = str(place.id)
        new_review = Review(**data)
        storage.new(new_review)
        storage.save()
        dict_ = new_review.to_dict()
        return jsonify(dict_), 201
    else:
        abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object
    """
    review = storage.get(Review, review_id)
    if review:
        data = request.get_json()
        if not data:
            return jsonify("Not a JSON"), 400
        keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in data.items():
            if key not in keys:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
