import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        return text(f"Received: {request.args}")

    request, response = app.test_client.get("/get_with_params?param1=value1&param2=value2")
    assert response.status == 200
    assert response.text == "Received: {'param1': ['value1'], 'param2': ['value2']}"