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

def test_get_method_without_slash(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_slash(app):
    request, response = app.test_client.get("/get/")
    assert response.status == 404  # Assuming strict slashes are enforced

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # No change in response for query params

def test_get_method_with_post_request(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405  # Method not allowed for GET route

def test_get_method_with_post_request_with_slash(app):
    request, response = app.test_client.post("/get/")
    assert response.status == 405  # Method not allowed for GET route with slash