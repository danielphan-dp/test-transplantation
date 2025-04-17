import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get_test")
    def handler(request: Request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get_test")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get_test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure query params do not affect response

def test_get_method_with_custom_headers(app):
    request, response = app.test_client.get("/get_test", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'  # Ensure custom headers do not affect response

def test_get_method_response_time(app):
    import time
    start_time = time.time()
    request, response = app.test_client.get("/get_test")
    end_time = time.time()
    assert response.status == 200
    assert (end_time - start_time) < 1  # Ensure response time is less than 1 second