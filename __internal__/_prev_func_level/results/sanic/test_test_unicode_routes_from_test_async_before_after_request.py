import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
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

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/get?name=test")
    assert response.text == 'I am get method'  # Assuming the method does not change based on query params

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_method(request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.text == ''