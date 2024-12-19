import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

def test_get_method_without_cookies(app):
    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_empty_cookies(app):
    cookies = {}

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", cookies=cookies)

    assert response.status == 200
    assert response.text == 'I am get method'
    assert len(request.cookies) == 0

def test_get_method_with_invalid_cookies(app):
    cookies = {"invalid": "cookie"}

    @app.get("/get")
    def handler(request):
        return text('I am get method')

    request, response = app.test_client.get("/get", cookies=cookies)

    assert response.status == 200
    assert response.text == 'I am get method'
    assert len(request.cookies) == 1
    assert request.cookies["invalid"] == "cookie"