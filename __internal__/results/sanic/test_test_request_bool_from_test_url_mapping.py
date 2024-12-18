import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.get("/get")
    def handler(request):
        return text(request.headers.get('X-Custom-Header', 'No Header'))

    request, response = app.test_client.get("/get", headers={'X-Custom-Header': 'HeaderValue'})
    assert response.text == "HeaderValue"
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.get("/get_empty")
    def handler(request):
        return text("")

    request, response = app.test_client.get("/get_empty")
    assert response.text == ""
    assert response.status == 200