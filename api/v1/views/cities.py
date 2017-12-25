#!/usr/bin/python3
"""module: states
contains flask api routing for City object queries"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def view_cities(state_id):
    """returns list of cities in a given state"""
    linked_state = storage.get("State", state_id)
    if linked_state is None:
        abort(404)
    city_list = [val.to_dict() for val in storage.all("City").values()]
    cities = [city for city in city_list if city['state_id'] == state_id]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def view_one_city(city_id):
    """returns one city"""
    a_city = storage.get("City", city_id)
    if a_city is None:
        abort(404)
    return jsonify(a_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """delete a city"""
    city_delete = storage.get("City", city_id)
    if city_delete is None:
        abort(404)
    storage.delete(city_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """add a city to storage"""
    linked_state = storage.get("State", state_id)
    if linked_state is None:
        abort(404)
    new_city = request.get_json()
    if new_city is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_city = json.loads(input_json) -- not necessary, new_city is a dict
    if new_city.get("name") is None:
        return jsonify({'error': "Missing name"}), 400
    new_city['state_id'] = state_id
    new_city = City(**new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a city & save the updates to storage"""
    city_data = request.get_json()
    if city_data is None:
        return jsonify({'error': "Not a JSON"}), 400

    # check if city_id is valid
    city_update = storage.get("City", city_id)
    if city_update is None:
        abort(404)
    no_updates = ['id', 'state_id', 'created_at', 'updated_at']
    for attr, value in city_data.items():
        if attr in no_updates:
            pass
        else:
            setattr(city_update, attr, value)
    city_update.save()
    return jsonify(city_update.to_dict()), 200
