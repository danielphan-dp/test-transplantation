import pytest
import flask

def test_post_create(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_create_with_data(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", json={"key": "value"})
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_create_with_invalid_method(app, client):
    @app.route("/create", methods=["GET"])
    def create():
        return 'Create'

    rv = client.get("/create")
    assert rv.status_code == 405

def test_post_create_no_data(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data="")
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_create_with_malformed_json(app, client):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data="malformed", content_type="application/json")
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200