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
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            return text(f'Query param: {request.args.get("param", "none")}')

    app.add_route(DummyView().get, "/get_with_param")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.text == 'Query param: test'
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/get_with_param/test")
    assert response.status == 404

def test_get_method_with_empty_response(app):
    class DummyView:
        def get(self, request):
            return text('')

    app.add_route(DummyView().get, "/get_empty")

    request, response = app.test_client.get("/get_empty")
    assert response.text == ''
    assert response.status == 200