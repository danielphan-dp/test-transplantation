import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/1")
    async def get_method(request):
        return text('I am get method')
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/1")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/1?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/1", headers={})
    assert response.status == 200
    assert response.text == 'I am get method'