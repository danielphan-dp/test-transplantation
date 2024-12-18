import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/query")
    def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_no_query_params(app):
    @app.get("/query")
    def query_handler(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query")
    assert response.text == "Query param: none"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.get("/headers")
    def headers_handler(request):
        return text(f"Header: {request.headers.get('X-Custom-Header', 'not set')}")

    request, response = app.test_client.get("/headers", headers={"X-Custom-Header": "value"})
    assert response.text == "Header: value"
    assert response.status == 200

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text