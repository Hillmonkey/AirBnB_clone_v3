#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify
from models.engine.file_storage import classes
from models import storage
import models

api_classes = {
    "amenities": classes["Amenity"],
    "cities": classes["City"],
    "places": classes["Place"],
    "reviews": classes["Review"],
    "states": classes["State"],
    "users": classes["User"]
}

'''
classes = {
    "amenities": models.amenity,
    "cities": models.city,
    "places": models.place,
    "reviews": models.review,
    "states": models.state,
    "users": models.user
}
'''


@app_views.route('/status')
def status_OK():
    """returns 'status: OK'"""
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """returns: number of objects by type"""
    stat_dict = {}
    for class_name, storage_class in api_classes.items():
        stat_dict[class_name] = storage.count(storage_class)
    return jsonify(stat_dict)
