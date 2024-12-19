import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")

    request, response = app.test_client.get("/test")

    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_params(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text(f"Query param value: {request.args.get('param', 'not provided')}")

    app.add_route(TestView.as_view(), "/test_query")

    request, response = app.test_client.get("/test_query?param=value")

    assert response.text == "Query param value: value"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")

    assert response.status == 404
    assert "Requested URL /invalid_route not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test_middleware")

    request, response = app.test_client.get("/test_middleware")

    assert response.text == "I am get method"
    assert type(results[0]) is Request

def test_get_method_response_with_custom_header(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method", headers={"X-Custom-Header": "value"})

    app.add_route(TestView.as_view(), "/test_custom_header")

    request, response = app.test_client.get("/test_custom_header")

    assert response.text == "I am get method"
    assert response.headers["X-Custom-Header"] == "value"