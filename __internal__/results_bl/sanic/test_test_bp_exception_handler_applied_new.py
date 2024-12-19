import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get_with_params")
    def get_with_params(request):
        return text('I am get method with params')

    _, response = app.test_client.get("/get_with_params?param=value")
    assert response.status == 200
    assert response.text == 'I am get method with params'