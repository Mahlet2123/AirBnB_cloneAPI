#!/usr/bin/python3
"""__init__ module"""
from flask import Blueprint

# Blueprint class is used to create modular and reusable sets of
# routes and views in Flask applications.


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
# Creates an instance of the Blueprint class named app_views

from api.v1.views.index import *

"""
The line from api.v1.views.index import * is used to import all objects
defined in the index module into the current namespace.

In this specific context, it is assumed that the index module contains
the route handlers and view functions for the API endpoints.
By importing all objects from index using the * wildcard,
the code ensures that all the routes and view functions defined
in index will be available in the current module.

This allows the app_views blueprint to register these routes and views when
it is used in the Flask application.
"""
from api.v1.views.states import *
