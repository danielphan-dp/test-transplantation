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
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test?param=value")
    assert response.status == 200
    assert response.text == 'I am get method with param: value'

def test_get_method_no_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test")
    assert response.status == 200
    assert response.text == 'I am get method with param: default'

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            return text('I am get method')

    app.add_route(TestView.as_view(), "/test")
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == 'I am get method'