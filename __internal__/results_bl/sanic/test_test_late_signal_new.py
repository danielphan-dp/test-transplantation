import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.status_code == 200
    assert response.text == 'I am get method'

def test_get_method_empty_request(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", headers={'Content-Length': '0'})
    assert response.status_code == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    _, response = app.test_client.get("/invalid")
    assert response.status_code == 404

def test_get_method_with_query_params(app):
    @app.get("/get")
    def handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    _, response = app.test_client.get("/get?param=test")
    assert response.status_code == 200
    assert response.text == 'Query param: test'