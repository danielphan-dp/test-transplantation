import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    return app

@pytest.mark.filterwarnings('ignore:Types other than str will be')
def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_response_not_a_string(app):
    @app.route("/get_invalid")
    async def get_invalid(request):
        return text(123)  # Invalid response type

    request, response = app.test_client.get("/get_invalid")
    assert response.status == 500
    assert b"Internal Server Error" in response.body

def test_get_method_empty_response(app):
    @app.route("/get_empty")
    async def get_empty(request):
        return text("")  # Empty string response

    request, response = app.test_client.get("/get_empty")
    assert response.status == 200
    assert response.text == ""