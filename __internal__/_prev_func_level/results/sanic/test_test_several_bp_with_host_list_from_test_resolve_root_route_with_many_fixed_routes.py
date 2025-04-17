import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    headers = {"Host": "example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"

def test_get_method_with_different_hosts(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    headers = {"Host": "sub.example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"

def test_get_method_with_invalid_host(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    headers = {"Host": "invalid.example.com"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == "I am get method"  # Ensure it still responds correctly

def test_get_method_no_host_header(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"  # Ensure it responds without host header

def test_get_method_multiple_requests(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    for _ in range(10):
        headers = {"Host": "example.com"}
        request, response = app.test_client.get("/get", headers=headers)
        assert response.text == "I am get method"