import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404
    assert "Requested URL /non_existent not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/get_with_params")
    async def handler(request):
        return text(f"Received param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.text == "Received param: test"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.route("/get_with_headers")
    async def handler(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header')}")

    request, response = app.test_client.get("/get_with_headers", headers={"X-Custom-Header": "value"})
    assert response.text == "Header value: value"
    assert response.status == 200