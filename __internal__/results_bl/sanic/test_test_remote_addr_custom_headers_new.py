import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test")
async def test_handler(request):
    return text('I am get method')

def test_get_method_default(app):
    request, response = app.test_client.get("/test")
    assert response.body == b'I am get method'

def test_get_method_with_custom_header(app):
    headers = {"X-Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/test", headers=headers)
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_no_headers(app):
    request, response = app.test_client.get("/test", headers={})
    assert response.body == b'I am get method'