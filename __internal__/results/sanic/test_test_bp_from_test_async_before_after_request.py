import pytest
from sanic import Sanic, Blueprint, text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def handler(request):
    return text('I am get method')

def test_get_method_success(app):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the handler does not change based on query params

def test_get_method_with_invalid_method(app):
    bp = Blueprint("Test", version=1)
    bp.route("/")(handler)
    app.blueprint(bp)

    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text