import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    app.route("/get")(lambda request: text("I am get method"))
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.body == b"I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get(
        "/get",
        headers={
            "FOO": "bar",
            "Host": "example.com",
            "User-Agent": "Sanic-Testing",
        },
    )
    assert response.status == 200
    assert response.body == b"I am get method"

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", data="")
    assert response.status == 200
    assert response.body == b"I am get method"