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
    assert response.text == "I am get method"
    assert response.status == 200

def test_request_server_name_in_host_header(app):
    request, response = app.test_client.get(
        "/", headers={"Host": "my-server:5555"}
    )
    assert request.server_name == "my-server"

    request, response = app.test_client.get(
        "/", headers={"Host": "[2a00:1450:400f:80c::200e]:5555"}
    )
    assert request.server_name == "[2a00:1450:400f:80c::200e]"

    request, response = app.test_client.get(
        "/", headers={"Host": "mal_formed"}
    )
    assert request.server_name == ""

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get(
        "/", headers={"Custom-Header": "CustomValue"}
    )
    assert response.text == "I am get method"
    assert response.status == 200
    assert request.headers.get("Custom-Header") == "CustomValue"

def test_get_method_with_empty_host_header(app):
    request, response = app.test_client.get(
        "/", headers={"Host": ""}
    )
    assert request.server_name == ""