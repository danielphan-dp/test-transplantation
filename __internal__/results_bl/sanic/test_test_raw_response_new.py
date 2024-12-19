import pytest
from sanic import Sanic
from sanic.response import text
from sanic.constants import DEFAULT_HTTP_CONTENT_TYPE

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.content_type == DEFAULT_HTTP_CONTENT_TYPE
    assert response.body == b'I am get method'

def test_get_method_empty_request(app):
    @app.get("/get_empty")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get_empty", headers={})
    assert response.content_type == DEFAULT_HTTP_CONTENT_TYPE
    assert response.body == b'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/get_with_query")
    def handler(request):
        return text('I am get method with query')

    request, response = app.test_client.get("/get_with_query?param=value")
    assert response.content_type == DEFAULT_HTTP_CONTENT_TYPE
    assert response.body == b'I am get method with query'