import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")

    @app.get("/")
    def handler(request):
        return text("I am get method")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/?param=value")
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_with_headers(app):
    headers = {"Custom-Header": "Value"}
    request, response = app.test_client.get("/", headers=headers)
    assert response.status == 200
    assert response.text == "I am get method"
    assert request.headers["Custom-Header"] == "Value"

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_cookies(app):
    cookies = {"test": "OK"}
    request, response = app.test_client.get("/", cookies=cookies)
    assert len(request.cookies) == len(cookies)
    assert request.cookies["test"] == cookies["test"]