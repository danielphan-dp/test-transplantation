import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_empty_query(app):
    request, response = app.test_client.get("/get?query=")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.status == 200
    assert response.body == b'I am get method'