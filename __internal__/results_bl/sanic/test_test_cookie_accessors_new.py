import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")

    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    _, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_headers(app):
    @app.get("/get_with_headers")
    async def handler(request):
        return text(f"Headers: {request.headers}")

    _, response = app.test_client.get("/get_with_headers", headers={"Custom-Header": "Value"})

    assert "Headers: {'custom-header': 'Value'}" in response.text

def test_get_method_with_empty_request(app):
    @app.get("/get_empty")
    async def handler(request):
        return text('I am get method with empty request')

    _, response = app.test_client.get("/get_empty", cookies={})

    assert response.text == 'I am get method with empty request'