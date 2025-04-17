import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def get_method(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_different_path(app):
    @app.get("/different")
    def different_get_method(request):
        return text('I am a different get method')

    request, response = app.test_client.get("/different")
    assert response.status == 200
    assert response.text == "I am a different get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_timeout(app):
    app.config.RESPONSE_TIMEOUT = 0.1
    response_middleware_run_count = 0

    @app.on_response
    def response(_, response):
        nonlocal response_middleware_run_count
        response_middleware_run_count += 1

    request, response = app.test_client.get("/")
    assert response_middleware_run_count == 1
    assert response.status == 200
    assert response.text == "I am get method"