import pytest
from sanic import Sanic, Request, json, text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("X-Custom-Header") is None

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'