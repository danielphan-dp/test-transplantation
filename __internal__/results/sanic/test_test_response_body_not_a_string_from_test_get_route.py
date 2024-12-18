import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_route(request):
        return text("I am get method")

    return app

@pytest.mark.filterwarnings('ignore:Types other than str will be')
def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_response_not_a_string(app):
    @app.route("/not_a_string")
    async def not_a_string_route(request):
        return text(123)  # Intentionally returning a non-string

    request, response = app.test_client.get("/not_a_string")
    assert response.status == 500
    assert b"Internal Server Error" in response.body

def test_get_method_empty_response(app):
    @app.route("/empty")
    async def empty_route(request):
        return text("")  # Testing empty string response

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""