import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get", methods=["GET"])
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("response")
    async def process_response(request, response):
        results.append(response)

    @app.route("/get_with_middleware", methods=["GET"])
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get_with_middleware")

    assert response.status == 200
    assert response.text == "I am get method"
    assert len(results) == 1
    assert isinstance(results[0], HTTPResponse)

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")

    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_invalid_method(app):
    @app.route("/get", methods=["GET"])
    async def get_handler(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")

    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text