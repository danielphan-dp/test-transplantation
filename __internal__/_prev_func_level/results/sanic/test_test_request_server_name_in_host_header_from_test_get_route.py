import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_host_header(app):
    request, response = app.test_client.get("/", headers={"Host": "my-server:5555"})
    assert request.server_name == "my-server"
    assert response.text == "I am get method"

def test_get_method_with_ipv6_host_header(app):
    request, response = app.test_client.get("/", headers={"Host": "[2a00:1450:400f:80c::200e]:5555"})
    assert request.server_name == "[2a00:1450:400f:80c::200e]"
    assert response.text == "I am get method"

def test_get_method_with_malformed_host_header(app):
    request, response = app.test_client.get("/", headers={"Host": "mal_formed"})
    assert request.server_name == ""
    assert response.text == "I am get method"