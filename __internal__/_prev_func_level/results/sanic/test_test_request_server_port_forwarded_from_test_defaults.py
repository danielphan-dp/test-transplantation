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

def test_get_method_with_custom_header(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get(
        "/get",
        headers={"Custom-Header": "CustomValue"}
    )
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("Custom-Header") == "CustomValue"

def test_get_method_with_invalid_route(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f"Query param foo: {request.args.get('foo')}")

    request, response = app.test_client.get("/get?foo=bar")
    assert response.text == "Query param foo: bar"
    assert response.status == 200

def test_get_method_with_no_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f"Query param foo: {request.args.get('foo')}")

    request, response = app.test_client.get("/get")
    assert response.text == "Query param foo: None"
    assert response.status == 200