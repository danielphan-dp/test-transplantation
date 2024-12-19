import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def handler(request):
    return text('I am get method')

def test_bp_use_route(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/", version=1.1)(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/v1.1")
    assert response.status == 200

def test_bp_get_method(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/get", version=1.1)(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/v1.1/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_bp_get_method_not_found(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/get", version=1.1)(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/v1.1/nonexistent")
    assert response.status == 404

def test_bp_get_method_invalid_version(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/get", version=1.1)(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/v2.0/get")
    assert response.status == 404