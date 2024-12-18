import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/")
    async def handler(request):
        return text("I am get method")

    return app

def test_get_method_status(app):
    request, response = app.test_client.get("/")
    assert response.status == 200

def test_get_method_response_text(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_headers(app):
    request, response = app.test_client.get("/")
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"