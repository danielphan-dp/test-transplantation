import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get", methods=["GET"])
    async def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_headers(app):
    @app.route("/get_with_headers", methods=["GET"])
    async def get_with_headers(request):
        return text(request.headers.get('X-Custom-Header', 'No Header'))

    headers = {"X-Custom-Header": "HeaderValue"}
    request, response = app.test_client.get("/get_with_headers", headers=headers)
    assert response.text == 'HeaderValue'
    assert response.status == 200

def test_get_method_with_query_params(app):
    @app.route("/get_with_query", methods=["GET"])
    async def get_with_query(request):
        return text(request.args.get('param', 'No Param'))

    request, response = app.test_client.get("/get_with_query?param=value")
    assert response.text == 'value'
    assert response.status == 200

def test_get_method_without_query_params(app):
    @app.route("/get_without_query", methods=["GET"])
    async def get_without_query(request):
        return text(request.args.get('param', 'No Param'))

    request, response = app.test_client.get("/get_without_query")
    assert response.text == 'No Param'
    assert response.status == 200