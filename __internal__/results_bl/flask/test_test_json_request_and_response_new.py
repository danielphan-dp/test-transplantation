import flask
import pytest
from flask import jsonify

def test_post_method(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    with client:
        # Test valid POST request
        rv = client.post("/create")
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'

        # Test POST request with JSON data
        json_data = {"item": "test"}
        rv = client.post("/create", json=json_data)
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'

        # Test POST request with invalid data type
        rv = client.post("/create", data="invalid data")
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'

        # Test POST request with no data
        rv = client.post("/create", json=None)
        assert rv.status_code == 200
        assert rv.data.decode() == 'Create'