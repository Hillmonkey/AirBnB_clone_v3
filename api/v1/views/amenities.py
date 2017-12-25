#!/usr/bin/python3
"""module: amenities
contains flask api routing for Amenity object queries"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def view_amenities():
    """returns list of amenities in a given state"""
    amenity_list = [val.to_dict() for val in storage.all("Amenity").values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def view_one_amenity(amenity_id):
    """returns one amenity"""
    an_amenity = storage.get("Amenity", amenity_id)
    if an_amenity is None:
        abort(404)
    return jsonify(an_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """delete an amenity"""
    amenity_delete = storage.get("Amenity", amenity_id)
    if amenity_delete is None:
        abort(404)
    storage.delete(amenity_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def add_amenity():
    """add an amenity to storage"""
    new_amenity = request.get_json()
    if new_amenity is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_amenity is a dict
    if new_amenity.get("name") is None:
        return jsonify({'error': "Missing name"}), 400
    new_amenity = Amenity(**new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """update an amenity & save the updates to storage"""
    amenity_data = request.get_json()
    if amenity_data is None:
        return jsonify({'error': "Not a JSON"}), 400
    amenity_update = storage.get("Amenity", amenity_id)
    if amenity_update is None:
        abort(404)
    no_updates = ['id', 'created_at', 'updated_at']
    for attr, value in amenity_data.items():
        if attr in no_updates:
            pass
        else:
            setattr(amenity_update, attr, value)
    amenity_update.save()
    return jsonify(amenity_update.to_dict()), 200
