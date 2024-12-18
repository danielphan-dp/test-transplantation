import pytest
import flask
from flask.json.provider import DefaultJSONProvider

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

class CustomProvider(DefaultJSONProvider):
    def object_hook(self, obj):
        if len(obj) == 1 and "_foo" in obj:
            return X(obj["_foo"])
        return obj

    def loads(self, s, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        return super().loads(s, **kwargs)

def test_post_create(app, client):
    app.json = CustomProvider(app)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create")
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_with_json(app, client):
    app.json = CustomProvider(app)

    @app.route("/create", methods=["POST"])
    def create():
        return flask.json.dumps(flask.request.get_json()["x"])

    rv = client.post(
        "/create",
        data=flask.json.dumps({"x": {"_foo": 42}}),
        content_type="application/json",
    )
    assert rv.data == b'"<42>"'
    assert rv.status_code == 200

def test_post_empty_body(app, client):
    app.json = CustomProvider(app)

    @app.route("/create", methods=["POST"])
    def create():
        return 'Create'

    rv = client.post("/create", data={})
    assert rv.data.decode() == 'Create'
    assert rv.status_code == 200

def test_post_invalid_json(app, client):
    app.json = CustomProvider(app)

    @app.route("/create", methods=["POST"])
    def create():
        return flask.json.dumps(flask.request.get_json()["x"])

    rv = client.post(
        "/create",
        data="invalid json",
        content_type="application/json",
    )
    assert rv.status_code == 400