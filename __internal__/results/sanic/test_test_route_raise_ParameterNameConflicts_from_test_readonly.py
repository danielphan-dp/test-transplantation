import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.get("/test")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_parameters(app):
    @app.get("/user/<username>")
    def handler(request, username):
        return text(f'Hello, {username}')

    request, response = app.test_client.get("/user/testuser")
    assert response.status == 200
    assert response.text == 'Hello, testuser'

def test_get_method_with_empty_parameters(app):
    @app.get("/user/")
    def handler(request):
        return text('No user provided')

    request, response = app.test_client.get("/user/")
    assert response.status == 200
    assert response.text == 'No user provided'