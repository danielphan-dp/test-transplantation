import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def middleware(request):
        results.append(request)

    request, response = app.test_client.get("/")
    assert response.text == 'I am get method'
    assert len(results) == 1
    assert results[0].path == '/'

def test_get_method_request_headers(app):
    request, response = app.test_client.get("/", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert request.headers.get("X-Custom-Header") == "value"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?foo=bar")
    assert response.status == 200
    assert response.text == 'I am get method'