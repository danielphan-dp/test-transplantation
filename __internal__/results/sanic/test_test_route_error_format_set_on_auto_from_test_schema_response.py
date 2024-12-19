import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change behavior with query params

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={"Content-Length": "0"})
    assert response.status == 200
    assert response.text == "I am get method"  # Assuming the method does not change behavior with empty request