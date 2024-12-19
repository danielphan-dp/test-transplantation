import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.get("/test")
async def test_handler(request):
    return text('I am get method')

def test_get_method(app):
    request_middleware_run_count = 0
    response_middleware_run_count = 0

    @app.on_response
    def response(_, response):
        nonlocal response_middleware_run_count
        response_middleware_run_count += 1

    @app.on_request
    def request(_):
        nonlocal request_middleware_run_count
        request_middleware_run_count += 1

    app.test_client.get("/test")
    assert request_middleware_run_count == 1
    assert response_middleware_run_count == 1

def test_get_method_empty_request(app):
    response = app.test_client.get("/test", headers={})
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method'