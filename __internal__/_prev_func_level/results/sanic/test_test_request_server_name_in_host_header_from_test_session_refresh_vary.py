import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_host_header(app):
    request, response = app.test_client.get("/get", headers={"Host": "my-server:5555"})
    assert request.server_name == "my-server"

    request, response = app.test_client.get("/get", headers={"Host": "[2a00:1450:400f:80c::200e]:5555"})
    assert request.server_name == "[2a00:1450:400f:80c::200e]"

    request, response = app.test_client.get("/get", headers={"Host": "mal_formed"})
    assert request.server_name == ""

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_empty_host(app):
    request, response = app.test_client.get("/get", headers={"Host": ""})
    assert request.server_name == ""