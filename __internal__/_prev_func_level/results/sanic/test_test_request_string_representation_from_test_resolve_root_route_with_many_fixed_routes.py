import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_repr(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, _ = app.test_client.get("/get")
    assert repr(request) == "<Request: GET /get>"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text(request.headers.get("X-Custom-Header", "No Header"))

    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "HeaderValue"})
    assert response.text == "HeaderValue"
    assert response.status == 200

def test_get_method_invalid_method(app):
    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text("I am get method")

    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text