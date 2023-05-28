#!/usr/bin/python3
"""
A Flask route defined within the api.v1.views blueprint.
It returns a JSON response with a status message.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """
    returns a JSON response with a status message
    when a GET request is made to the /status URL.
    """
    return jsonify({"status": "OK"})

@app_views.route('/api/v1/stats')
def stats():
    """
    Returns the count of all objects by type
    """
