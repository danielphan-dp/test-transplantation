import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.get("/test_get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/test_get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_with_query_params(app):
    @app.get("/test_get_with_query")
    def get_method_with_query(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/test_get_with_query?param=value")
    assert response.status == 200
    assert response.text == 'Query param: value'

def test_get_method_with_empty_query_params(app):
    @app.get("/test_get_with_empty_query")
    def get_method_with_empty_query(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/test_get_with_empty_query")
    assert response.status == 200
    assert response.text == 'Query param: none'