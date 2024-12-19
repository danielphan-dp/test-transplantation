import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'  # Ensure it still returns the same response

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'  # Test with no additional data

def test_get_method_type(app):
    request, response = app.test_client.get("/get")
    assert isinstance(response, HTTPResponse)  # Check response type