import pytest
from sanic import Sanic
from sanic.response import text

app = Sanic("TestApp")

@app.get("/test")
def get_method(request):
    return text('I am get method')

@pytest.fixture
def test_app():
    return app

def test_get_method_success(test_app):
    request, response = test_app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(test_app):
    request, response = test_app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(test_app):
    request, response = test_app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'