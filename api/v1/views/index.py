#!/usr/bin/python3
"""
A Flask route defined within the api.v1.views blueprint.

The api.v1.views blueprint is important
because it allows for modular organization and
separation of routes and views in a Flask application.

It returns a JSON response with a status message.
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route("/status")
def status():
    """
    returns a JSON response with a status message
    when a GET request is made to the /status URL.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """
    retrieves the number of each objects by type
    """
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User,
    }
    ret_dict = {}
    for key, value in classes.items():
        ret_dict[key] = storage.count(value)
    return jsonify(ret_dict)
