import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test")
    assert response.body == b"I am get method"

def test_post_method_not_allowed(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.post("/test")
    assert b"Method POST not allowed for URL /test" in response.body

def test_get_method_with_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text(f"I am get method with param: {request.args.get('param')}")

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test?param=value")
    assert response.body == b"I am get method with param: value"

def test_get_method_with_empty_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text(f"I am get method with param: {request.args.get('param', 'default')}")

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test?param=")
    assert response.body == b"I am get method with param: default"