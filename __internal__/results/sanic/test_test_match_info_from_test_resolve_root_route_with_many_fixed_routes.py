import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/api/v1/test_get")
    async def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/api/v1/test_get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/api/v1/invalid_route")

    assert response.status == 404
    assert "Requested URL /api/v1/invalid_route not found" in response.text

def test_get_method_with_query_params(app):
    @app.route("/api/v1/test_get_with_params")
    async def handler(request):
        return text(f'Query param: {request.args.get("param", "none")}')

    request, response = app.test_client.get("/api/v1/test_get_with_params?param=test")

    assert response.status == 200
    assert response.text == 'Query param: test'