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

def test_get_method_with_headers(app):
    @app.route("/get_with_headers")
    async def handler(request):
        return text(f"Headers: {request.headers}")

    headers = {"Custom-Header": "TestValue"}
    request, response = app.test_client.get("/get_with_headers", headers=headers)
    assert response.text == 'Headers: {' + f'"Custom-Header": "TestValue"' + '}'
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.route("/get_with_query")
    async def handler(request):
        return text(f"Query Params: {request.args}")

    request, response = app.test_client.get("/get_with_query?param1=value1&param2=value2")
    assert response.text == 'Query Params: {' + '"param1": ["value1"], "param2": ["value2"]' + '}'
    assert response.status == 200

def test_get_method_with_empty_response(app):
    @app.route("/get_empty")
    async def handler(request):
        return text('')

    request, response = app.test_client.get("/get_empty")
    assert response.text == ''
    assert response.status == 200

def test_get_method_with_large_payload(app):
    @app.route("/get_large")
    async def handler(request):
        return text('Large payload received')

    request, response = app.test_client.get("/get_large")
    assert response.text == 'Large payload received'
    assert response.status == 200

def test_get_method_with_special_characters(app):
    @app.route("/get_special")
    async def handler(request):
        return text('Special characters: !@#$%^&*()')

    request, response = app.test_client.get("/get_special")
    assert response.text == 'Special characters: !@#$%^&*()'
    assert response.status == 200