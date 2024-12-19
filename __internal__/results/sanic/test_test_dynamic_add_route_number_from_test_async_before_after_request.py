import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    def get(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get")
    def get(request):
        return text(f'I am get method with query param: {request.args.get("param", "None")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.text == 'I am get method with query param: test'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/get/invalid")
    assert response.status == 404

def test_get_method_with_empty_response(app):
    @app.get("/empty")
    def empty_get(request):
        return text('')

    request, response = app.test_client.get("/empty")
    assert response.text == ''
    assert response.status == 200