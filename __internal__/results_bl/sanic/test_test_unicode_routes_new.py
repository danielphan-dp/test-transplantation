import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    def get_handler(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_unicode(app):
    request, response = app.test_client.get("/get?param=你好")
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_query(app):
    request, response = app.test_client.get("/get?param=")
    assert response.text == 'I am get method'