import pytest
from sanic import Sanic
from sanic.response import text
from sanic.request import Request
from sanic.response import HTTPResponse

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_method(request):
    return text('I am get method')

def test_get_method_response(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert isinstance(response, HTTPResponse)

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_middleware(app):
    results = []

    @app.on_request()
    async def process_request(request):
        results.append(request)

    @app.on_response()
    async def process_response(request, response):
        results.append(request)
        results.append(response)

    request, response = app.test_client.get("/get")

    assert response.text == 'I am get method'
    assert type(results[0]) is Request
    assert isinstance(results[1], Request)
    assert isinstance(results[2], HTTPResponse)