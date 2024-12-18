import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure the response is unaffected by query params

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure the response is unaffected by headers

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get")
    assert response.headers['Content-Type'] == 'text/plain; charset=utf-8'