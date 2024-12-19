import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_headers(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get",
        headers={"Custom-Header": "CustomValue"}
    )
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_empty_request(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", data="")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_query_parameters(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200