import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_query_params(app):
    @app.route("/get_with_params")
    def get_with_params(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Query param: test"

def test_get_method_with_headers(app):
    @app.route("/get_with_headers")
    def get_with_headers(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'none')}")

    request, response = app.test_client.get("/get_with_headers", headers={"X-Custom-Header": "value"})
    assert response.text == "Header value: value"