import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_socket_info(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")

    socket = request.socket
    assert isinstance(socket, tuple)

    ip = socket[0]
    port = socket[1]

    assert ip == request.ip
    assert port == request.port

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f"Query param: {request.args.get('param', 'not found')}")

    request, response = app.test_client.get("/get?param=test")

    assert response.status == 200
    assert response.text == "Query param: test"