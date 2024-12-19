import pytest
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method(app):
    @app.route("/get")
    def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route(app):
    @app.route("/get")
    def get_handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    
    assert response.status == 404

def test_get_method_with_cookie(app):
    @app.route("/get_with_cookie")
    def get_handler(request):
        response = text('I am get method')
        response.cookies["test"] = "cookie_value"
        response.cookies["test"]["httponly"] = True
        return response

    request, response = app.test_client.get("/get_with_cookie")
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get("Set-Cookie", {}))

    assert response_cookies["test"].value == "cookie_value"
    assert response_cookies["test"]["httponly"] is True

def test_get_method_with_expired_cookie(app):
    @app.route("/get_with_expired_cookie")
    def get_handler(request):
        response = text('I am get method')
        response.cookies["expired_test"] = "expired_value"
        response.cookies["expired_test"]["expires"] = datetime.now() - timedelta(seconds=10)
        return response

    request, response = app.test_client.get("/get_with_expired_cookie")
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get("Set-Cookie", {}))

    assert "expired_test" not in response_cookies

def test_get_method_with_multiple_cookies(app):
    @app.route("/get_with_multiple_cookies")
    def get_handler(request):
        response = text('I am get method')
        response.cookies["cookie1"] = "value1"
        response.cookies["cookie2"] = "value2"
        return response

    request, response = app.test_client.get("/get_with_multiple_cookies")
    response_cookies = SimpleCookie()
    response_cookies.load(response.headers.get("Set-Cookie", {}))

    assert response_cookies["cookie1"].value == "value1"
    assert response_cookies["cookie2"].value == "value2"