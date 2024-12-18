import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def get_handler(request):
        return text(f"Query param: {request.args.get('param', 'None')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Query param: test"

def test_get_method_with_headers(app):
    @app.route("/get")
    async def get_handler(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'None')}")

    headers = {"X-Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "Header value: CustomValue"

def test_get_method_with_empty_response(app):
    @app.route("/get")
    async def get_handler(request):
        return text("")

    request, response = app.test_client.get("/get")
    assert response.text == ""

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_invalid_method(app):
    @app.route("/get", methods=["GET"])
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_special_characters(app):
    @app.route("/get")
    async def get_handler(request):
        return text("Special characters: !@#$%^&*()")

    request, response = app.test_client.get("/get")
    assert response.text == "Special characters: !@#$%^&*()"