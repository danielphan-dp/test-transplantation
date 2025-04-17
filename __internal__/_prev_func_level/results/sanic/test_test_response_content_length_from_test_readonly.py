import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_method")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_method")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_content_type(app):
    request, response = app.test_client.get("/get_method")
    assert response.headers.get("Content-Type") == "text/plain; charset=utf-8"

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get_method", params={})
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/get_method?param=value")
    assert response.status == 200
    assert response.text == "I am get method"