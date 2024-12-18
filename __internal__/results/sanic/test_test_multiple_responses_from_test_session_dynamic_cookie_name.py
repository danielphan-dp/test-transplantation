import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.status == 200
    assert response.text == "I am get method"
    assert "Custom-Header" in response.headers

def test_get_method_empty_response(app):
    @app.get("/empty")
    def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.status == 200
    assert response.text == ""

def test_get_method_with_logging(app, caplog):
    with caplog.at_level("INFO"):
        request, response = app.test_client.get("/get")
        assert response.status == 200
        assert "I am get method" in caplog.text