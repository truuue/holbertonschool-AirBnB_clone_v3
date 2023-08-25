#!/usr/bin/python3
"""A first api app"""

from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from api.v1.views import app_views
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)
swagger = Swagger(app)


@app.errorhandler(404)
def invalide_route(e):
    """Returns a JSON if page not found"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == '__main__':
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = int(getenv("HBNB_API_PORT", 5000))
    app.run(host=host, port=port, threaded=True)
