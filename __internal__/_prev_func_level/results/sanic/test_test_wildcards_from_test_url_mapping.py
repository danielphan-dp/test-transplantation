import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    async def handler(request):
        return text(f"Query param: {request.args.get('param')}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.status == 200
    assert response.text == "Query param: test"

def test_get_method_with_headers(app):
    @app.get("/get_with_headers")
    async def handler(request):
        return text(request.headers.get('X-Custom-Header', 'No Header'))

    request, response = app.test_client.get("/get_with_headers", headers={'X-Custom-Header': 'HeaderValue'})
    assert response.status == 200
    assert response.text == "HeaderValue"

def test_get_method_no_content_type(app):
    @app.get("/get_no_content_type")
    async def handler(request):
        return text("No Content Type")

    request, response = app.test_client.get("/get_no_content_type")
    assert response.status == 200
    assert response.text == "No Content Type"
    assert response.content_type == "text/plain; charset=utf-8"