import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_different_http_methods(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text