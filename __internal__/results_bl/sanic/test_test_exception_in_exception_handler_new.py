import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/test_get")
    def test_get(request):
        return text('I am get method')
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/test_get?param=value")
    assert response.status == 200
    assert response.body == b'I am get method'  # Assuming the method does not change behavior with params

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/test_get")
    assert response.status == 405  # Method Not Allowed