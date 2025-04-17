import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    @app.middleware("response")
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    class MiddlewareView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(MiddlewareView.as_view(), "/")

    request, response = app.test_client.get("/")

    assert response.text == "I am get method"
    assert type(results[0]) is Request
    assert isinstance(results[1], Request)
    assert isinstance(results[2], HTTPResponse)

def test_get_method_with_custom_header(app):
    class CustomHeaderView(HTTPMethodView):
        def get(self, request):
            return text("I am get method", headers={"X-Custom-Header": "value"})

    app.add_route(CustomHeaderView.as_view(), "/")

    request, response = app.test_client.get("/")

    assert response.status == 200
    assert response.headers["X-Custom-Header"] == "value"