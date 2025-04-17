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
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.route("/get")
    async def handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/get?param=test")
    assert response.text == 'Query param: test'
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.route("/get")
    async def handler(request):
        return text(f'Header: {request.headers.get("X-Custom-Header", "none")}')

    headers = {"X-Custom-Header": "custom_value"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'Header: custom_value'
    assert response.status == 200

def test_get_method_with_empty_response(app):
    @app.route("/get_empty")
    async def handler(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.text == ''
    assert response.status == 200

def test_get_method_with_large_response(app):
    @app.route("/get_large")
    async def handler(request):
        return text('A' * 10000)

    request, response = app.test_client.get("/get_large")
    assert response.text == 'A' * 10000
    assert response.status == 200

def test_get_method_with_special_characters(app):
    @app.route("/get_special")
    async def handler(request):
        return text('Special characters: !@#$%^&*()')

    request, response = app.test_client.get("/get_special")
    assert response.text == 'Special characters: !@#$%^&*()'
    assert response.status == 200