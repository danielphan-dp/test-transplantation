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
        return str(json.get("value", 0))

    rv = client.post(
        "/create",
        data=flask.json.dumps({"value": 5}),
        content_type="application/json",
    )
    assert rv.data == b'5'

def test_post_create_no_data(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data={})
    assert rv.data == b'Create'