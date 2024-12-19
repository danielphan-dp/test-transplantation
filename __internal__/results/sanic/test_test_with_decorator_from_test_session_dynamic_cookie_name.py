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
    assert response.text == "I am get method"

def test_get_method_with_different_route(app):
    class AnotherView(HTTPMethodView):
        def get(self, request):
            return text("I am another get method")

    app.add_route(AnotherView.as_view(), "/another")

    request, response = app.test_client.get("/another")
    assert response.text == "I am another get method"

def test_get_method_with_query_param(app):
    class QueryView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    app.add_route(QueryView.as_view(), "/query")

    request, response = app.test_client.get("/query?param=test")
    assert response.text == "Received param: test"

def test_get_method_with_no_query_param(app):
    class QueryView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    app.add_route(QueryView.as_view(), "/query")

    request, response = app.test_client.get("/query")
    assert response.text == "Received param: default"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_decorator(app):
    results = []

    def sample_decorator(view):
        def decorator(*args, **kwargs):
            results.append(1)
            return view(*args, **kwargs)
        return decorator

    class DecoratedView(HTTPMethodView):
        decorators = [sample_decorator]

        def get(self, request):
            return text("I am get method with decorator")

    app.add_route(DecoratedView.as_view(), "/decorated")

    request, response = app.test_client.get("/decorated")
    assert response.text == "I am get method with decorator"
    assert results[0] == 1