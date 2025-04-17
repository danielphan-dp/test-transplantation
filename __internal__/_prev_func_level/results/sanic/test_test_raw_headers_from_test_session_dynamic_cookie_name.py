import pytest
from sanic import Sanic
from sanic.text import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    app.route("/get")(lambda request: text("I am get method"))
    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_custom_headers(app):
    request, response = app.test_client.get(
        "/get",
        headers={
            "Custom-Header": "CustomValue",
            "User-Agent": "Sanic-Testing",
        },
    )
    assert response.text == "I am get method"
    assert response.status == 200
    assert b"Custom-Header: CustomValue" in request.raw_headers
    assert b"User-Agent: Sanic-Testing" in request.raw_headers

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert b"Requested URL /invalid not found" in response.text

def test_get_method_with_empty_request(app):
    request, response = app.test_client.get("/get", data="")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_query_parameters(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200