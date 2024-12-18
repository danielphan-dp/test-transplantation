import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import ServerError

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_server_error(app):
    @app.exception(ServerError)
    def handler_exception(request, exception):
        return text("Internal Server Error.", 500)

    @app.route("/error")
    async def handler(request):
        raise ServerError("This is a server error")

    request, response = app.test_client.get("/error")
    assert response.status == 500
    assert response.body == b"Internal Server Error."