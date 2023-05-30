#!/usr/bin/python3
"""
app module that sets up a Flask application
registers blueprints, and defines a teardown function
"""
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def remove_session(exception):
    """a Flask teardown function.
    It is executed after each request to the Flask application."""
    storage.close()


@app_views.errorhandler(404)
def not_found(error):
    """Handler for 404 errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")
    app.run(host=host, port=port, threaded=True)
