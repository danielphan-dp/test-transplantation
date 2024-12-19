import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get_method", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get_method")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_with_invalid_method(app):
    @app.route("/get_method", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.post("/get_method")
    assert response.status == 405
    assert "Method POST not allowed for URL /get_method" in response.text

def test_multiple_get_methods(app):
    @app.route("/duplicate_get", methods=["GET"])
    async def first_get(request):
        return text("First GET method")

    @app.route("/duplicate_get", methods=["GET"])
    async def second_get(request):
        return text("Second GET method")

    request, response = app.test_client.get("/duplicate_get")
    assert response.status == 200
    assert response.text == "First GET method"  # Should return the first registered handler

def test_get_method_with_query_params(app):
    @app.route("/get_with_params", methods=["GET"])
    async def get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Received param: {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

    request, response = app.test_client.get("/get_with_params")
    assert response.text == "Received param: default"
    assert response.status == 200