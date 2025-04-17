import pytest
from sanic import Sanic
from sanic.response import text
from sanic.constants import DEFAULT_HTTP_CONTENT_TYPE

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.content_type == DEFAULT_HTTP_CONTENT_TYPE
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_param")
    def handler(request):
        return text(f'Query param received: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == 'Query param received: test'
    assert response.status == 200

def test_get_method_empty_response(app):
    @app.get("/get_empty")
    def handler(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.text == ''
    assert response.status == 200
    assert response.content_type == DEFAULT_HTTP_CONTENT_TYPE