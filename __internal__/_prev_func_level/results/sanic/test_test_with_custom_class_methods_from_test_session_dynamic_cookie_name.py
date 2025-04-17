import pytest
from sanic import Sanic
from sanic.response import text
from sanic.views import HTTPMethodView

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            name = request.args.get('name', 'Guest')
            return text(f'I am get method, hello {name}')

    app.add_route(TestView.as_view(), "/greet")
    request, response = app.test_client.get("/greet?name=Alice")
    assert response.text == "I am get method, hello Alice"

def test_get_method_with_no_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            name = request.args.get('name', 'Guest')
            return text(f'I am get method, hello {name}')

    app.add_route(TestView.as_view(), "/greet")
    request, response = app.test_client.get("/greet")
    assert response.text == "I am get method, hello Guest"

def test_get_method_with_custom_header(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text('I am get method with custom header')

    app.add_route(TestView.as_view(), "/custom-header")
    request, response = app.test_client.get("/custom-header", headers={"X-Custom-Header": "value"})
    assert response.text == "I am get method with custom header"