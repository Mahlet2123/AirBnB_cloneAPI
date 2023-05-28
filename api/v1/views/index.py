#!/usr/bin/python3
"""
A Flask route defined within the api.v1.views blueprint.
It returns a JSON response with a status message.
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    return jsonify({"status": "OK"})
