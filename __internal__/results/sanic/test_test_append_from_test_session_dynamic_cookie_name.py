import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def json_app():
    app = Sanic("test_app")
    return app

def test_get_method(json_app):
    @json_app.get("/get")
    async def handler_get(request):
        return text('I am get method')

    request, response = json_app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(json_app):
    request, response = json_app.test_client.get("/non-existent")
    assert response.status == 404

def test_get_method_with_query_param(json_app):
    @json_app.get("/get")
    async def handler_get(request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    request, response = json_app.test_client.get("/get?param=test")
    assert response.text == 'I am get method with param: test'
    assert response.status == 200

def test_get_method_with_invalid_method(json_app):
    @json_app.get("/get")
    async def handler_get(request):
        return text('I am get method')

    request, response = json_app.test_client.post("/get")
    assert response.status == 405
    assert "Method POST not allowed for URL /get" in response.text