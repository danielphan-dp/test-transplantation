import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_server_name(app):
    request, response = app.test_client.get("/get")
    assert request.server_name == "127.0.0.1"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_with_empty_query_params(app):
    @app.get("/get_with_empty_param")
    def handler(request):
        return text(f"Received param: {request.args.get('param', 'default')}")

    request, response = app.test_client.get("/get_with_empty_param")
    assert response.text == "Received param: default"
    assert response.status == 200