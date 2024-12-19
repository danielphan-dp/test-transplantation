import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/test_get")
    def test_get(request):
        return text('I am get method')

    _, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert b'I am get method' in response.body

def test_get_method_not_found(app):
    @app.get("/test_get")
    def test_get(request):
        return text('I am get method')

    _, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_query_param(app):
    @app.get("/test_get")
    def test_get(request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    _, response = app.test_client.get("/test_get?param=test")
    assert response.status == 200
    assert b'I am get method with param: test' in response.body

def test_get_method_empty_query_param(app):
    @app.get("/test_get")
    def test_get(request):
        return text(f'I am get method with param: {request.args.get("param", "none")}')

    _, response = app.test_client.get("/test_get?param=")
    assert response.status == 200
    assert b'I am get method with param: none' in response.body