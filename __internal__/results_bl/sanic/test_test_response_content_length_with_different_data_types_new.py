import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    async def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'
    assert response.headers.get("Content-Length") == "20"

def test_get_method_empty_request(app):
    _, response = app.test_client.get("/get", headers={"Content-Length": "0"})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    _, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method'