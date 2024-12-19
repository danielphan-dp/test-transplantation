import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/get")
    def get_method(request):
        return text('I am get method')
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_invalid_request(app):
    request, response = app.test_client.get("/get", query_string={"invalid": "param"})
    assert response.status == 200
    assert response.text == "I am get method"