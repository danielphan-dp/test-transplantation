import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/test")
    def get_method(request: Request):
        return text("I am get method")

    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/test")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid_route")
    assert response.status == 404

def test_get_method_with_no_auth(app):
    request, response = app.test_client.get("/test", headers={})
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/test", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") == "value"  # Assuming the header is passed through