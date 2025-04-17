import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200
    assert "Custom-Header" in request.headers

def test_get_method_with_ipv6_address(app):
    request, response = app.test_client.get("/get", host="::1")
    assert response.text == 'I am get method'
    assert request.ip == "::1"