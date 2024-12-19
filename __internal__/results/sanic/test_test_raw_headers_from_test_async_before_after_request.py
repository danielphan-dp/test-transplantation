import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method_response(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    request, response = app.test_client.get(
        "/get",
        headers={
            "FOO": "bar",
            "Host": "example.com",
            "User-Agent": "Sanic-Testing",
        },
    )

    assert response.status == 200
    assert response.text == "I am get method"
    assert b"Host: example.com" in request.raw_headers
    assert b"User-Agent: Sanic-Testing" in request.raw_headers
    assert b"FOO: bar" in request.raw_headers

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.text

def test_get_method_with_empty_response(app):
    @app.route("/get_empty")
    def get_empty(request):
        return text("")

    request, response = app.test_client.get("/get_empty")
    
    assert response.status == 200
    assert response.text == ""