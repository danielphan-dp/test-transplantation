import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/")
    def get(request):
        return text('I am get method')
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 405

def test_get_method_empty_path(app):
    request, response = app.test_client.get("")
    assert response.status == 404