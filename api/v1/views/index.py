#!/usr/bin/python3
"""A index file"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify


@app_views.route("/status")
def status():
    """Return status of the server"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Return stats of the objects"""
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    count_dict = {}
    for name, cls in classes.items():
        count_dict[name] = storage.count(cls)
    return jsonify(count_dict)
