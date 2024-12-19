import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def handler(request):
    return text('I am get method')

def test_bp(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/v1")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/v1")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_bp_invalid_route(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/v1")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_bp_method_not_allowed(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/v1")(handler)
    app.blueprint(bp)

    _, response = app.test_client.post("/v1")
    assert response.status == 405

def test_bp_empty_request(app, handler):
    bp = Blueprint("Test", version=1)
    bp.route("/v1")(handler)
    app.blueprint(bp)

    _, response = app.test_client.get("/v1", headers={'Content-Length': '0'})
    assert response.status == 200
    assert response.text == 'I am get method'