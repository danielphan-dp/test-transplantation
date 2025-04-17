import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.route("/get")
    def get_method(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response

def test_get_method_empty_response(app):
    @app.route("/empty")
    def empty_response(request):
        return text("")

    request, response = app.test_client.get("/empty")
    assert response.text == ""
    assert response.status == 200

def test_get_method_with_cookies(app):
    @app.route("/set_cookie")
    def set_cookie(request):
        response = text("Cookie set")
        response.cookies["test_cookie"] = "cookie_value"
        return response

    request, response = app.test_client.get("/set_cookie")
    assert response.cookies.get("test_cookie") == "cookie_value"
    assert response.status == 200

def test_get_method_cookie_deletion(app):
    @app.route("/delete_cookie")
    def delete_cookie(request):
        response = text("Cookie deleted")
        del response.cookies["test_cookie"]
        return response

    request, response = app.test_client.get("/delete_cookie")
    assert "test_cookie" not in response.cookies
    assert response.status == 200