import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_test")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_test")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_test?param=value")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"