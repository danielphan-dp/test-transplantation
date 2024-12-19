import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get_method")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    _, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_content_length(app):
    _, response = app.test_client.get("/get_method")
    content_length = response.headers.get("Content-Length")
    assert content_length == str(len('I am get method'))