import pytest
import flask
from flask.json.provider import DefaultJSONProvider

class X:  # noqa: B903, for Python2 compatibility
    def __init__(self, val):
        self.val = val

def default(o):
    if isinstance(o, X):
        return f"<{o.val}>"
    return DefaultJSONProvider.default(o)

class CustomProvider(DefaultJSONProvider):
    def object_hook(self, obj):
        if len(obj) == 1 and "_foo" in obj:
            return X(obj["_foo"])
        return obj

    def loads(self, s, **kwargs):
        kwargs.setdefault("object_hook", self.object_hook)
        return super().loads(s, **kwargs)

@pytest.fixture
def app():
    app = flask.Flask(__name__)
    app.json = CustomProvider(app)
    app.json.default = default
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@app.route("/create", methods=["POST"])
def create():
    return 'Create'

def test_create_endpoint(client):
    rv = client.post("/create")
    assert rv.data == b'Create'

def test_create_with_json(client):
    rv = client.post(
        "/create",
        data=flask.json.dumps({"x": {"_foo": 42}}),
        content_type="application/json",
    )
    assert rv.data == b'Create'

def test_create_with_empty_json(client):
    rv = client.post(
        "/create",
        data=flask.json.dumps({}),
        content_type="application/json",
    )
    assert rv.data == b'Create'

def test_create_with_invalid_json(client):
    rv = client.post(
        "/create",
        data="invalid json",
        content_type="application/json",
    )
    assert rv.status_code == 400

def test_create_with_missing_json_key(client):
    rv = client.post(
        "/create",
        data=flask.json.dumps({"y": {"_foo": 42}}),
        content_type="application/json",
    )
    assert rv.data == b'Create'