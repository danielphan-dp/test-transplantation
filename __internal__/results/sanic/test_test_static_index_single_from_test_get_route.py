import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.headers["Content-Type"] == "text/plain; charset=utf-8"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    
    assert response.status == 404
    assert "Requested URL /nonexistent not found" in response.text

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param is {param}')

    app.add_route(DummyView().get, "/get_with_param")

    request, response = app.test_client.get("/get_with_param?param=test")
    
    assert response.status == 200
    assert response.text == "Param is test"

def test_get_method_with_empty_query_param(app):
    class DummyView:
        def get(self, request):
            param = request.args.get('param', 'default')
            return text(f'Param is {param}')

    app.add_route(DummyView().get, "/get_with_param")

    request, response = app.test_client.get("/get_with_param?param=")
    
    assert response.status == 200
    assert response.text == "Param is "