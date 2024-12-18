import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    @app.route("/get_with_headers")
    def handler(request):
        response = text("I am get method with headers")
        response.headers["X-Custom-Header"] = "CustomValue"
        return response

    request, response = app.test_client.get("/get_with_headers")
    assert response.headers["X-Custom-Header"] == "CustomValue"
    assert response.text == "I am get method with headers"
    assert response.status == 200

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", data={})
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.route("/get_with_query")
    def handler(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

    request, response = app.test_client.get("/get_with_query")
    assert response.text == "Received param: default"
    assert response.status == 200