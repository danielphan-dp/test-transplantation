import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")

    request, response = app.test_client.get("/test")

    assert response.text == "I am get method"

def test_get_method_empty_request(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test_empty")

    request, response = app.test_client.get("/test_empty")

    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method with query params")

    app.add_route(TestView.as_view(), "/test_query")

    request, response = app.test_client.get("/test_query?param=value")

    assert response.text == "I am get method with query params"

def test_get_method_with_middleware(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test_middleware")

    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    request, response = app.test_client.get("/test_middleware")

    assert response.text == "I am get method"
    assert type(results[0]) is Request

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")

    assert response.status == 404