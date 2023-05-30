#!/usr/bin/python3
"""
app module that sets up a Flask application
registers blueprints, and defines a teardown function

first endpoint (route) will be to return the status of your API
if we do not import those modules in the __init__.py file, we have to
manually register each routes in the flask app. Eg:
    app.register_blueprint(states.app_views)
    app.register_blueprint(cities.app_views)
    app.register_blueprint(amenities.app_views) ...
Since, we imported the modules in the __init__.py file whereby the app_views
blueprint is registered, we can just only register the 'app_views' blueprint
so that the flask app can access all the routes and method in each module.
In this case the 'app_views' blueprint is used as the container having all
the routes and methods within the modules.

Additionally, When we import the app_views blueprint into the module and
also import the modules into the __init__.py file, you don't need to manually
register each module in the Flask app. The registration happens automatically
when the routes are defined within the modules using the app_views blueprint.
"""

from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
app.register_blueprint(app_views)

@app.teardown_appcontext
def remove_session(exception):
    """ a Flask teardown function.
    It is executed after each request to the Flask application. """
    storage.close()

@app_views.errorhandler(404)
def not_found(error):
    """ Handler for 404 errors """
    return make_response(jsonify({"error": "Not found"}), 404)

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
