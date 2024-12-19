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

def test_get_method_with_forwarded_headers(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get(
        "/get",
        headers={
            "Host": "my-server:5555",
            "X-Forwarded-For": "127.1.2.3",
            "X-Forwarded-Port": "4444",
        },
    )
    assert response.text == 'I am get method'
    assert request.server_port == 4444

def test_get_method_invalid_route(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_no_headers(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={})
    assert response.text == 'I am get method'
    assert response.status == 200