import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
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

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent")
    assert response.status == 404

def test_get_method_with_query_param(app):
    class DummyView:
        def get(self, request):
            return text(f"I am get method with param: {request.args.get('param', 'None')}")

    app.add_route(DummyView().get, "/get_with_param")

    request, response = app.test_client.get("/get_with_param?param=test")
    assert response.status == 200
    assert response.text == "I am get method with param: test"

def test_get_method_empty_query_param(app):
    class DummyView:
        def get(self, request):
            return text(f"I am get method with param: {request.args.get('param', 'None')}")

    app.add_route(DummyView().get, "/get_with_param")

    request, response = app.test_client.get("/get_with_param?param=")
    assert response.status == 200
    assert response.text == "I am get method with param: "