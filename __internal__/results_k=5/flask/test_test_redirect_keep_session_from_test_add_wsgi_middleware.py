import pytest
import flask

def test_post_create(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    with client:
        rv = client.post("/create")
        assert rv.data == b'Create'

def test_post_create_with_data(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        data = flask.request.form.get("data")
        if data:
            return f'Created with data: {data}'
        return 'Create'

    with client:
        rv = client.post("/create", data={"data": "test"})
        assert rv.data == b'Created with data: test'

def test_post_create_no_data(client, app):
    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    with client:
        rv = client.post("/create", data={})
        assert rv.data == b'Create'