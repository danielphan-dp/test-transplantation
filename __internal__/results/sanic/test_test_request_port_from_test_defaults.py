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

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get_method")
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_method_with_params")
    def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_method_with_params?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_no_params(app):
    @app.get("/get_method_no_params")
    def handler(request):
        return text("No params received")

    request, response = app.test_client.get("/get_method_no_params")
    assert response.text == "No params received"
    assert response.status == 200