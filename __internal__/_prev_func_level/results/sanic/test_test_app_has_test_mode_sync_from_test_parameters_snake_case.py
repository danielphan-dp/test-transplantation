import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test")
    return app

def test_get_method_response(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def handler(request):
        return text(f"Received params: {request.args}")

    request, response = app.test_client.get("/get_with_params?param1=value1&param2=value2")
    assert response.status == 200
    assert response.text == "Received params: {'param1': ['value1'], 'param2': ['value2']}"

def test_get_method_with_empty_query_params(app):
    @app.get("/get_empty_params")
    def handler(request):
        return text(f"Received params: {request.args}")

    request, response = app.test_client.get("/get_empty_params")
    assert response.status == 200
    assert response.text == "Received params: {}"