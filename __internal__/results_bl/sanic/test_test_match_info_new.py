import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.route("/api/v1/test/")
    async def test_get(request):
        return text('I am get method')
    return app

def test_get_method(app):
    request, response = app.test_client.get("/api/v1/test/")
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/api/v1/test/?query=")
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/api/v1/invalid/")
    assert response.status == 404

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/api/v1/test/", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'