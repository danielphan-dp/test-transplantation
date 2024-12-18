import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def handler(request):
        return text(f'I am get method with query param: {request.args.get("param")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.status == 200
    assert response.text == 'I am get method with query param: test'

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    @app.route("/get")
    async def handler(request):
        return text(f'Header value: {request.headers.get("X-Custom-Header")}')

    headers = {"X-Custom-Header": "CustomValue"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.status == 200
    assert response.text == 'Header value: CustomValue'

def test_get_method_with_empty_response(app):
    @app.route("/get_empty")
    async def handler(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.status == 200
    assert response.text == ''