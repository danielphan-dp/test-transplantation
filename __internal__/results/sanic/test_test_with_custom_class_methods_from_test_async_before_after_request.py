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

    app.add_route(TestView.as_view(), "/get")
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"

def test_get_method_with_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(TestView.as_view(), "/get")
    request, response = app.test_client.get("/get?param=test")
    assert response.text == "I am get method with param: test"

def test_get_method_with_no_query_param(app):
    class TestView(HTTPMethodView):
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'I am get method with param: {param}')

    app.add_route(TestView.as_view(), "/get")
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method with param: default"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_internal_logic(app):
    class TestView(HTTPMethodView):
        global_var = 0

        def _internal_method(self):
            self.global_var += 5

        def get(self, request):
            self._internal_method()
            return text(f'I am get method and global var is {self.global_var}')

    app.add_route(TestView.as_view(), "/get")
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method and global var is 5"