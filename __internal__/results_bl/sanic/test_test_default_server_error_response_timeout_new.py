import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    @app.get("/1")
    def get_method(request):
        return text('I am get method')
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/1")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/1?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_service_unavailable(app, response_timeout_default_app):
    request, response = response_timeout_default_app.test_client.get("/1")
    assert response.status == 503
    assert "Response Timeout" in response.text