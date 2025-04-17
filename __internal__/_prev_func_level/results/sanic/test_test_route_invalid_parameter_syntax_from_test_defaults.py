import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import InvalidUsage

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_valid(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    with pytest.raises(InvalidUsage):
        request, response = app.test_client.get("/get/<:str>")

def test_get_method_no_parameters(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_parameter(app):
    request, response = app.test_client.get("/get/invalid_param")
    assert response.status == 404
    assert "Requested URL /get/invalid_param not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert len(results) == 1
    assert results[0].path == "/get"