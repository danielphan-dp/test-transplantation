import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_ipv6_address(app):
    request, response = app.test_client.get("/get", host="::1")
    assert response.status == 200
    assert request.ip == "::1"  # Assuming the request object has an ip attribute

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/get", headers={"X-Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure the response is unaffected by the header

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure the response is unaffected by query parameters