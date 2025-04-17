import flask
import pytest

def test_post_create(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_with_invalid_method(app, client):
    @app.route("/create", methods=["GET"])
    def create():
        return 'Create'

    rv = client.get("/create")
    assert rv.status_code == 405

def test_post_create_with_no_data(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data={})
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_with_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        json = flask.request.get_json()
        return str(json.get("message", "Create"))

    rv = client.post(
        "/create",
        json={"message": "New Post"},
        content_type="application/json",
    )
    assert rv.data == b'New Post'
    assert rv.status_code == 200

def test_post_create_with_empty_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        json = flask.request.get_json()
        return str(json.get("message", "Create"))

    rv = client.post(
        "/create",
        json={},
        content_type="application/json",
    )
    assert rv.data == b'Create'
    assert rv.status_code == 200