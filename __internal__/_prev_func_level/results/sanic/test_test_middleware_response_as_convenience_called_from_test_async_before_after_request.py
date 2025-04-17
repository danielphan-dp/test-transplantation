import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.response import HTTPResponse

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

def test_get_method_type(app):
    request, response = app.test_client.get("/get")
    assert isinstance(response, HTTPResponse)

def test_get_method_request_type(app):
    results = []

    @app.on_request()
    async def process_request(request):
        results.append(request)

    request, response = app.test_client.get("/get")
    
    assert type(results[0]) is Request

def test_get_method_multiple_requests(app):
    results = []

    @app.on_request()
    async def process_request(request):
        results.append(request)

    for _ in range(5):
        app.test_client.get("/get")

    assert len(results) == 5
    for req in results:
        assert isinstance(req, Request)