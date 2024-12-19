import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    class DummyView:
        def get(self, request):
            return text('I am get method')

    app.add_route(DummyView().get, "/get")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"
    assert response.content_type == "text/plain; charset=utf-8"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_headers(app):
    class DummyView:
        def get(self, request):
            return text('I am get method with headers')

    app.add_route(DummyView().get, "/get-headers")

    request, response = app.test_client.get("/get-headers", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method with headers"
    assert response.content_type == "text/plain; charset=utf-8"