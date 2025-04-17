import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status_code == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status_code == 404

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status_code == 405
    assert "Method POST not allowed for URL /get" in response.text