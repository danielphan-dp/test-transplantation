import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_response_headers(app):
    request, response = app.test_client.get("/get")
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "text/plain; charset=utf-8"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={})
    assert response.status == 200
    assert response.text == 'I am get method'