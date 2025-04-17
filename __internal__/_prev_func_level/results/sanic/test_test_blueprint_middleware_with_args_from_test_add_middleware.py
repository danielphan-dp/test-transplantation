import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_different_content_type(app):
    request, response = app.test_client.get("/", headers={"Accept": "application/json"})
    assert response.text == "I am get method"  # Assuming the method does not change behavior based on Accept header

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"  # Assuming the method does not change behavior based on query parameters