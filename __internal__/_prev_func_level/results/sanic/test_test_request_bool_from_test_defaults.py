import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_method")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_request_object(app):
    request, response = app.test_client.get("/get_method")
    assert bool(request)

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_method?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get_method", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("X-Custom-Header") == "value"