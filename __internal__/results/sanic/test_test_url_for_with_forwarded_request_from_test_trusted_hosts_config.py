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

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_forwarded_headers(app):
    request, response = app.test_client.get(
        "/get",
        headers={
            "X-Forwarded-For": "192.168.1.1",
            "X-Forwarded-Proto": "http",
            "X-Forwarded-Port": "8080",
        },
    )
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get(
        "/get",
        headers={"Custom-Header": "CustomValue"},
    )
    assert response.status == 200
    assert response.text == "I am get method"