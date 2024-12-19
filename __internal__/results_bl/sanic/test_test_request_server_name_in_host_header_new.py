import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_with_valid_host(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get", headers={"Host": "valid-server:8080"}
    )
    assert response.text == 'I am get method'

def test_get_method_with_empty_host(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get", headers={"Host": ""}
    )
    assert response.text == 'I am get method'

def test_get_method_with_malformed_host(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get", headers={"Host": "mal_formed"}
    )
    assert response.text == 'I am get method'

def test_get_method_with_ipv6_host(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get", headers={"Host": "[::1]:8080"}
    )
    assert response.text == 'I am get method'