import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.response import HTTPResponse

@pytest.fixture
def app():
    app = Sanic("test_app")

    class DummyView:
        def get(self, request):
            return text("I am get method")

    app.add_route(DummyView().get, "/")

    return app

def test_get_method_response(app):
    request, response = app.test_client.get("/")
    assert response.text == "I am get method"
    assert response.status == 200

def test_get_method_type(app):
    request, response = app.test_client.get("/")
    assert isinstance(request, Request)
    assert isinstance(response, HTTPResponse)

def test_get_method_with_middleware(app):
    results = []

    @app.middleware("request")
    async def process_request(request):
        results.append(request)

    @app.middleware("response")
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    request, response = app.test_client.get("/")

    assert response.text == "I am get method"
    assert type(results[0]) is Request
    assert type(results[1]) is Request
    assert isinstance(results[2], HTTPResponse)

def test_get_method_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header(app):
    request, response = app.test_client.get("/", headers={"Custom-Header": "Value"})
    assert response.text == "I am get method"
    assert response.status == 200
    assert response.headers.get("Custom-Header") is None  # No custom header in response