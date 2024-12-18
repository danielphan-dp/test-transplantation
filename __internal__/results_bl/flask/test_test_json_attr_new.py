import pytest
import flask
import flask.json

def test_post_create(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data == b'Create'

def test_post_create_with_data(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        json = flask.request.get_json()
        return str(json.get("message", "Create"))

    rv = client.post(
        "/create",
        data=flask.json.dumps({"message": "New Item"}),
        content_type="application/json",
    )
    assert rv.data == b'New Item'

def test_post_create_empty_data(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        json = flask.request.get_json()
        return str(json.get("message", "Create"))

    rv = client.post(
        "/create",
        data=flask.json.dumps({}),
        content_type="application/json",
    )
    assert rv.data == b'Create'

def test_post_create_invalid_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data="invalid json", content_type="application/json")
    assert rv.data == b'Create'