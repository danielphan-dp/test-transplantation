import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get-method")
    async def get_method(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get-method")
    assert response.text == "I am get method"

def test_get_method_status_code(app):
    request, response = app.test_client.get("/get-method")
    assert response.status == 200

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get-method")
    assert response.content_type == "text/plain; charset=utf-8"