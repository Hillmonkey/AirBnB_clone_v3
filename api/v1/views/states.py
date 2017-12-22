#!/usr/bin/python3
"""module: states
contains flask api routing for state object queries"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def view_states():
    """returns list of states"""
    """ if no states, returns an empty list with status code 200"""
    state_list = [val.to_dict() for val in storage.all("State").values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def view_one_state(state_id):
    """returns one state"""
    a_state = storage.get("State", state_id)
    if a_state is None:
        abort(404)
    return jsonify(a_state.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_state():
    """add a state to storage"""
    new_state = request.get_json()
    if new_state is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_state = json.loads(input_json) -- not necessary, new_state is a dict
    if new_state.get("name") is None:
        return jsonify({'error': "Missing name"}), 400
    new_state = State(**new_state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state & save the updates to storage"""
    state_data = request.get_json()
    if state_data is None:
        return jsonify({'error': "Not a JSON"}), 400

    state_update = storage.get("State", state_id)
    if state_update is None:
        abort(404)
    no_updates = ['id', 'created_at', 'updated_at']
    for attr, value in state_data.items():
        if attr in no_updates:
            pass
        else:
            setattr(state_update, attr, value)
    state_update.save()
    return jsonify(state_update.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    state_delete = storage.get("State", state_id)
    if state_delete is None:
        abort(404)
    storage.delete(state_delete)
    return jsonify({})
