import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    async def test_get(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_status_code(app):
    request, response = app.test_client.get("/test")
    assert response.status == 200

def test_get_method_content_type(app):
    request, response = app.test_client.get("/test")
    assert response.content_type == "text/plain; charset=utf-8"