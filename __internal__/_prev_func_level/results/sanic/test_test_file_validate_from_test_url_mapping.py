import pytest
from sanic import Sanic, Request
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    def get_method(request: Request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_headers(app):
    @app.route("/get_with_headers", methods=["GET"])
    def get_method_with_headers(request: Request):
        return text('I am get method with headers')

    request, response = app.test_client.get("/get_with_headers", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method with headers'
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_with_query_params(app):
    @app.route("/get_with_query", methods=["GET"])
    def get_method_with_query(request: Request):
        param = request.args.get("param", "default")
        return text(f'Query param is {param}')

    request, response = app.test_client.get("/get_with_query?param=test")
    assert response.status == 200
    assert response.text == 'Query param is test'

    request, response = app.test_client.get("/get_with_query")
    assert response.status == 200
    assert response.text == 'Query param is default'