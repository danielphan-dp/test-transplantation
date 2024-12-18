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

def test_get_method_with_custom_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'
    assert request.headers.get("Custom-Header") == "value"

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the method does not change based on query params

def test_get_method_with_different_accept_headers(app):
    header_value = "application/json"
    request, response = app.test_client.get("/get", headers={"Accept": header_value})
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the method does not change based on Accept header

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/get", data="")
    assert response.status == 200
    assert response.text == 'I am get method'  # Assuming the method does not change based on empty data