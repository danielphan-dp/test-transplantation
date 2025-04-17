import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.headers.get("Custom-Header") == "value"

def test_get_method_invalid_route(app):
    @app.get("/valid")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.body

def test_get_method_with_query_params(app):
    @app.get("/")
    async def handler(request):
        return text(f"I am get method with param: {request.args.get('param')}")

    request, response = app.test_client.get("/?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"