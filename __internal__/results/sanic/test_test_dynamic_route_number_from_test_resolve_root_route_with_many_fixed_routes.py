import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method with query")

    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method with query"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.get("/")
    async def handler(request):
        return text("I am get method with headers")

    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method with headers"
    assert response.status == 200

def test_get_method_with_empty_response(app):
    @app.get("/")
    async def handler(request):
        return text("")

    request, response = app.test_client.get("/")
    assert response.text == ""
    assert response.status == 200

def test_get_method_with_non_string_response(app):
    @app.get("/")
    async def handler(request):
        return text(123)  # This should raise a TypeError

    with pytest.raises(TypeError):
        app.test_client.get("/")