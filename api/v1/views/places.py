#!/usr/bin/python3
"""module: places
contains flask api routing for Place object queries"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def view_places(city_id):
    """returns list of places in a given state"""
    linked_city = storage.get("City", city_id)
    if linked_city is None:
        abort(404)
    place_list = [val.to_dict() for val in storage.all("Place").values()]
    places = [place for place in place_list if place['city_id'] == city_id]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def view_one_place(place_id):
    """returns one place"""
    a_place = storage.get("Place", place_id)
    if a_place is None:
        abort(404)
    return jsonify(a_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete a place"""
    place_delete = storage.get("Place", place_id)
    if place_delete is None:
        abort(404)
    storage.delete(place_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """add a place to storage"""
    linked_city = storage.get("City", city_id)
    if linked_city is None:
        abort(404)
    new_place = request.get_json()
    if new_place is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_place = json.loads(input_json) -- not necessary, new_place is a dict
    if new_place.get("user_id") is None:
        return jsonify({'error': "Missing user_id"}), 400

    linked_user = storage.get("User", new_place.get("user_id"))
    if linked_user is None:
        abort(404)
    if new_place.get("name") is None:
        return jsonify({'error': "Missing name"}), 400
    new_place['city_id'] = city_id
    new_place = Place(**new_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """update a place & save the updates to storage"""
    place_data = request.get_json()
    if place_data is None:
        return jsonify({'error': "Not a JSON"}), 400

    # check if place_id is valid
    place_update = storage.get("Place", place_id)
    if place_update is None:
        abort(404)
    no_updates = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for attr, value in place_data.items():
        if attr in no_updates:
            pass
        else:
            setattr(place_update, attr, value)
    place_update.save()
    return jsonify(place_update.to_dict()), 200
