import pytest
import flask
import json

def test_post_create(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_with_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        json_data = flask.request.get_json()
        return json_data.get("message", "Create")

    rv = client.post(
        "/create",
        data=json.dumps({"message": "New Item"}),
        content_type="application/json",
    )
    assert rv.data == b'New Item'
    assert rv.status_code == 200

def test_post_create_no_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data={})
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_invalid_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post(
        "/create",
        data="invalid json",
        content_type="application/json",
    )
    assert rv.data == b'Create'
    assert rv.status_code == 200