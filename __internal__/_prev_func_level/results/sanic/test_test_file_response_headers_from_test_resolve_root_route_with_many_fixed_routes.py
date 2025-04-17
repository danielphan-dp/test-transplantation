import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.mark.parametrize('path', ['/test', '/another_test'])
def test_get_method(app: Sanic, path: str):
    @app.route(path, methods=["GET"])
    def get_route(request: Request):
        return text('I am get method')

    request, response = app.test_client.get(path)
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app: Sanic):
    request, response = app.test_client.get('/invalid_route')
    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_query_params(app: Sanic):
    @app.route("/test_query", methods=["GET"])
    def get_query_route(request: Request):
        return text(f"Query param: {request.args.get('param', 'not found')}")

    request, response = app.test_client.get('/test_query?param=value')
    assert response.status == 200
    assert response.text == "Query param: value"

def test_get_method_with_empty_query_params(app: Sanic):
    @app.route("/test_empty_query", methods=["GET"])
    def get_empty_query_route(request: Request):
        return text(f"Query param: {request.args.get('param', 'not found')}")

    request, response = app.test_client.get('/test_empty_query')
    assert response.status == 200
    assert response.text == "Query param: not found"