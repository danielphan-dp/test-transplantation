import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_test")
    def handler(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_test_with_params")
    def handler(request: Request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_test_with_params?param=test")
    assert response.status == 200
    assert response.text == "Received param: test"

def test_get_method_no_params(app):
    request, response = app.test_client.get("/get_test_with_params")
    assert response.status == 200
    assert response.text == "Received param: default"