import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/test")
    assert response.text == 'I am get method'

def test_get_method_with_unicode(app):
    @app.get("/你好")
    def handler(request):
        return text('I am get method with unicode')

    request, response = app.test_client.get("/你好")
    assert response.text == 'I am get method with unicode'

def test_get_method_with_query_param(app):
    @app.get("/test_query")
    def handler(request):
        return text(f'I am get method with query param: {request.args.get("param", "")}')

    request, response = app.test_client.get("/test_query?param=value")
    assert response.text == 'I am get method with query param: value'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404
    assert "Requested URL /non_existent_route not found" in response.text

def test_get_method_invalid_method(app):
    @app.get("/test")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.post("/test")
    assert response.status == 405
    assert "Method POST not allowed for URL /test" in response.text