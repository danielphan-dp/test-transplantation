import pytest
import flask
from flask.json.provider import DefaultJSONProvider

def test_post_method(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data.decode() == 'Create'

def test_post_method_with_data(app, client):
    @app.route("/create_with_data", methods=["POST"])
    def create_with_data():
        data = flask.request.get_json()
        return data.get("message", "No message provided")

    rv = client.post(
        "/create_with_data",
        data=flask.json.dumps({"message": "Hello"}),
        content_type="application/json",
    )
    assert rv.data.decode() == 'Hello'

def test_post_method_empty_data(app, client):
    @app.route("/create_empty", methods=["POST"])
    def create_empty():
        data = flask.request.get_json()
        return data.get("message", "No message provided")

    rv = client.post(
        "/create_empty",
        data=flask.json.dumps({}),
        content_type="application/json",
    )
    assert rv.data.decode() == 'No message provided'

def test_post_method_invalid_json(app, client):
    @app.route("/create_invalid_json", methods=["POST"])
    def create_invalid_json():
        return 'Invalid JSON', 400

    rv = client.post("/create_invalid_json", data="invalid json", content_type="application/json")
    assert rv.status_code == 400
    assert rv.data.decode() == 'Invalid JSON'