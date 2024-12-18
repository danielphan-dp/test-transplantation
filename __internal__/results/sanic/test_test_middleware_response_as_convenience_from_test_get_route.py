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
    assert response.status == 200
    assert response.text == "I am get method"

def test_get_method_type(app):
    request, response = app.test_client.get("/")
    assert isinstance(response, HTTPResponse)

def test_get_method_request_type(app):
    request, response = app.test_client.get("/")
    assert isinstance(request, Request)

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
    assert isinstance(results[1], Request)
    assert isinstance(results[2], HTTPResponse)
    assert type(results[3]) is Request
    assert isinstance(results[4], HTTPResponse)