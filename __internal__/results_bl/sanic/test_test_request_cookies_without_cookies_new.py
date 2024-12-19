import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_request_cookies_with_cookies(app):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", cookies={"session_id": "12345"})

    assert request.cookies == {"session_id": "12345"}
    assert response.text == "I am get method"

def test_request_cookies_empty(app):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/")

    assert request.cookies == {}
    assert response.text == "I am get method"

def test_request_cookies_multiple_cookies(app):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", cookies={"session_id": "12345", "user_id": "abcde"})

    assert request.cookies == {"session_id": "12345", "user_id": "abcde"}
    assert response.text == "I am get method"

def test_request_cookies_invalid_cookie(app):
    @app.get("/")
    def handler(request):
        return text("I am get method")

    request, response = app.test_client.get("/", cookies={"invalid_cookie": None})

    assert request.cookies == {"invalid_cookie": None}
    assert response.text == "I am get method"