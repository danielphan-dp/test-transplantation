import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status_code == 404

def test_get_method_empty_request(app):
    @app.get("/empty")
    def handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/empty", data="")
    assert response.status_code == 200
    assert response.text == 'I am get method'