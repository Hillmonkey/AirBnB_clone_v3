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
    state_list = [val.to_dict() for val in storage.all("State").values()]
    return jsonify(state_list)

@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def view_one_state(id):
    """returns one state"""
    a_state = storage.get("State", id)
    if a_state is None:
        abort(404)
    return jsonify(a_state.to_dict())

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_a_state():
    """add a state to storage"""
    new_state = request.get_json()
    if new_state == None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_state = json.loads(input_json) -- not necessary, new_state is a dict
    if new_state.get("name") == None:
        return jsonify({'error': "Missing name"}), 400
    new_state = State(**new_state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201
