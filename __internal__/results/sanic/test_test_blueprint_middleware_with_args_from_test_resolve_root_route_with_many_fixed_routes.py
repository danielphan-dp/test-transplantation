import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request: Request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"

def test_get_method_with_invalid_method(app):
    request, response = app.test_client.post("/")
    assert response.status == 405
    assert "Method POST not allowed for URL /" in response.text

def test_get_method_with_empty_path(app):
    request, response = app.test_client.get("")
    assert response.status == 404
    assert "Requested URL / not found" in response.text

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get("/?param=value")
    assert response.text == "I am get method"