import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    async def get(request):
        return text('I am get method')

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_route_assigned(app):
    request, _ = app.test_client.get("/")
    assert request.route is list(app.router.routes)[0]

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    @app.get("/query")
    async def get_with_query(request):
        return text(f"Query param: {request.args.get('param', 'none')}")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Query param: test"
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.get("/headers")
    async def get_with_headers(request):
        return text(f"Header value: {request.headers.get('X-Custom-Header', 'none')}")

    request, response = app.test_client.get("/headers", headers={"X-Custom-Header": "value"})
    assert response.text == "Header value: value"
    assert response.status == 200