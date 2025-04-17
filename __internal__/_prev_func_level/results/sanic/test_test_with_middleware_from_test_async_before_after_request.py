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

def test_get_method_with_middleware(app):
    results = []

    @app.middleware
    async def handler(request):
        results.append(request)

    class TestView(HTTPMethodView):
        def get(self, request):
            return text("I am get method")

    app.add_route(TestView.as_view(), "/test")

    request, response = app.test_client.get("/test")

    assert response.text == "I am get method"
    assert type(results[0]) is Request

def test_get_method_with_custom_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text("Custom response", status=201)

    app.add_route(TestView.as_view(), "/custom")

    request, response = app.test_client.get("/custom")

    assert response.text == "Custom response"
    assert response.status == 201

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")

    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f"Received param: {param}")

    app.add_route(TestView.as_view(), "/query")

    request, response = app.test_client.get("/query?param=test")

    assert response.text == "Received param: test"
    assert response.status == 200

    request, response = app.test_client.get("/query")

    assert response.text == "Received param: default"
    assert response.status == 200