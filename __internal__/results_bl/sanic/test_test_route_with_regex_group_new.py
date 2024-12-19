import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test/get")
async def get_method(request):
    return text('I am get method')

def test_get_method(app):
    _, response = app.test_client.get("/test/get")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    _, response = app.test_client.get("/test/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    _, response = app.test_client.get("/test/get?param=value")
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    _, response = app.test_client.get("/test/get")
    assert response.text == 'I am get method'