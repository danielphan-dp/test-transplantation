import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test_get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_forwarded_headers(app):
    request, response = app.test_client.get(
        "/test_get",
        headers={
            "X-Forwarded-For": "192.168.1.1",
            "X-Forwarded-Proto": "http",
            "X-Forwarded-Port": "8080",
        },
    )
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test_get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"