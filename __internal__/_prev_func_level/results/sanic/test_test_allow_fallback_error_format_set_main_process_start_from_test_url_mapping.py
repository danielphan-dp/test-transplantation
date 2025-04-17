import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_custom_header(app):
    @app.get("/get_with_header")
    async def get_method_with_header(request):
        return text('I am get method with header', headers={'X-Custom-Header': 'value'})

    request, response = app.test_client.get("/get_with_header")
    assert response.status == 200
    assert response.headers['X-Custom-Header'] == 'value'