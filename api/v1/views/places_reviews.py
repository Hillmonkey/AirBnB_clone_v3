#!/usr/bin/python3
"""module: reviews
contains flask api routing for Review object queries"""
from api.v1.views import app_views
from flask import abort, jsonify, request
import json
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from mdoels.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def view_reviews(place_id):
    """returns list of reivews for a given place"""
    linked_place = storage.get("Place", place_id)
    if linked_place is None:
        abort(404)
    review_list = [val.to_dict() for val in storage.all("Review").values()]
    reviews = [review for review in review_list
               if review['place_id'] == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def view_one_review(review_id):
    """returns one review"""
    a_review = storage.get("Review", review_id)
    if a_review is None:
        abort(404)
    return jsonify(a_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """delete a review"""
    review_delete = storage.get("Review", review_id)
    if review_delete is None:
        abort(404)
    storage.delete(review_delete)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def add_review(place_id):
    """add a review to storage"""
    linked_place = storage.get("Place", place_id)
    if linked_place is None:
        abort(404)
    new_review = request.get_json()
    if new_review is None:
        return jsonify({'error': "Not a JSON"}), 400
    # new_review is a dict
    if new_review.get("user_id") is None:
        return jsonify({'error': "Missing user_id"}), 400

    linked_user = storage.get("User", new_review.get("user_id"))
    if linked_user is None:
        abort(404)
    if new_review.get("text") is None:
        return jsonify({'error': "Missing text"}), 400
    new_review['place_id'] = place_id
    new_review = Review(**new_review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update a review & save the updates to storage"""
    review_data = request.get_json()
    if review_data is None:
        return jsonify({'error': "Not a JSON"}), 400

    # check if review_id is valid
    review_update = storage.get("Review", review_id)
    if review_update is None:
        abort(404)
    no_updates = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for attr, value in review_data.items():
        if attr in no_updates:
            pass
        else:
            setattr(review_update, attr, value)
    review_update.save()
    return jsonify(review_update.to_dict()), 200
