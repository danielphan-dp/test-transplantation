import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    def get_handler(request):
        return text('I am get method')
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_socket_info(app):
    request, response = app.test_client.get("/get")
    socket = request.socket
    assert isinstance(socket, tuple)

    ip = socket[0]
    port = socket[1]

    assert ip == request.ip
    assert port == request.port

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={'Content-Length': '0'})
    assert response.status == 200
    assert response.text == 'I am get method'