#!/usr/bin/python3
"""module: users
contains flask api routing for User object queries"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def view_users():
    """returns list of users in a given state"""
    user_list = [val.to_dict() for val in storage.all("User").values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def view_one_user(user_id):
    """returns one user"""
    a_user = storage.get("User", user_id)
    if a_user is None:
        abort(404)
    return jsonify(a_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """delete a user"""
    user_delete = storage.get("User", user_id)
    if user_delete is None:
        abort(404)
    storage.delete(user_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def add_user():
    """add an user to storage"""
    new_user = request.get_json()
    if new_user is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_user is a dict
    if new_user.get("email") is None:
        return jsonify({'error': "Missing email"}), 400
    if new_user.get("password") is None:
        return jsonify({'error': "Missing password"}), 400
    new_user = User(**new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """update an user & save the updates to storage"""
    user_data = request.get_json()
    if user_data is None:
        return jsonify({'error': "Not a JSON"}), 400
    user_update = storage.get("User", user_id)
    if user_update is None:
        abort(404)
    no_updates = ['id', 'email', 'created_at', 'updated_at']
    for attr, value in user_data.items():
        if attr in no_updates:
            pass
        else:
            setattr(user_update, attr, value)
    user_update.save()
    return jsonify(user_update.to_dict()), 200
