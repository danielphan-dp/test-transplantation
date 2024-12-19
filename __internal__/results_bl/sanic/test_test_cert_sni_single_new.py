import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test_get")
async def test_get_handler(request):
    return text('I am get method')

def test_get_method(app):
    port = app.test_client.port
    _, response = app.test_client.get(f"http://localhost:{port}/test_get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    port = app.test_client.port
    _, response = app.test_client.get(f"http://localhost:{port}/non_existent")
    assert response.status == 404

def test_get_method_empty_request(app):
    port = app.test_client.port
    _, response = app.test_client.get(f"http://localhost:{port}/test_get", data="")
    assert response.status == 200
    assert response.text == "I am get method"