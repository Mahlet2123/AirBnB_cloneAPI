#!/usr/bin/python3
""" app module """
from models import storage
from flask import Flask
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)
# Register the app_views blueprint
app.register_blueprint(app_views)

@app.teardown_appcontext
def remove_session(exception):
    """ a Flask teardown function.
    It is executed after each request to the Flask application. """
    storage.close()

if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
