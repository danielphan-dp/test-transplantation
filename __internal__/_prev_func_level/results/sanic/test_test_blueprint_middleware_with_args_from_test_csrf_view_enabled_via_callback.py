import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_custom_header(app):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_different_content_type(app):
    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", headers={"Accept": "application/json"})
    assert response.text == 'I am get method'
    assert response.status == 200