import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_custom_headers(app):
    @app.route("/")
    async def handler(request):
        return text('I am get method')

    headers = {"X-Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_empty_request(app):
    @app.route("/")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'