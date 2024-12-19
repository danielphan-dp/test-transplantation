import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.response import HTTPResponse
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

    app.add_route(TestView.as_view(), "/empty")

    request, response = app.test_client.get("/empty", headers={})

    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method with query params")

    app.add_route(TestView.as_view(), "/query")

    request, response = app.test_client.get("/query?param=value")

    assert response.text == "I am get method with query params"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404

def test_get_method_with_middleware_response(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    @app.middleware("response")
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/middleware")

    request, response = app.test_client.get("/middleware")

    assert response.text == "I am get method"
    assert type(results[0]) is Request
    assert isinstance(results[1], Request)
    assert isinstance(results[2], HTTPResponse)