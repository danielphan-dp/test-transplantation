import uuid
import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/")
    async def get(request):
        return text('I am get method')
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_route(app):
    request, _ = app.test_client.get("/")
    assert request.route is list(app.router.routes)[0]

def test_get_method_empty_query(app):
    request, response = app.test_client.get("/?query=")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.body == b'I am get method'