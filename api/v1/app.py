#!/usr/bin/python3
"""module: app"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_close(exception):
    """method: teardown_close"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """method: page_not_found"""
    return jsonify(error="Not found"), 404

if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port)
