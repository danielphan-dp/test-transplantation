import pytest
import flask

def test_post_create(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_with_data(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data={"key": "value"})
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_empty_data(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data={})
    assert rv.data == b'Create'
    assert rv.status_code == 200

def test_post_create_invalid_method(client, app):
    @app.route("/create", methods=["GET"])
    def create():
        return 'Create'

    rv = client.get("/create")
    assert rv.status_code == 405  # Method Not Allowed

def test_post_create_with_headers(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", headers={"Content-Type": "application/json"})
    assert rv.data == b'Create'
    assert rv.status_code == 200