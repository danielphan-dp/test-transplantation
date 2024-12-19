import pytest
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import SanicException

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/get")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_empty_path(app):
    request, response = app.test_client.get("/")
    assert response.status == 404

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405