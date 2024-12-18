import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def get_with_params(request):
        return text(f"Received param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_no_params(app):
    @app.get("/get_no_params")
    def get_no_params(request):
        return text("No params received")

    request, response = app.test_client.get("/get_no_params")
    assert response.text == "No params received"
    assert response.status == 200

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    def get_with_header(request):
        return text(f"Header received: {request.headers.get('X-Custom-Header', 'none')}")

    request, response = app.test_client.get("/get_with_header", headers={"X-Custom-Header": "test-header"})
    assert response.text == "Header received: test-header"
    assert response.status == 200