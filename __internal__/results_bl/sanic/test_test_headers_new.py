import pytest
from sanic import Sanic
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("TestApp")
    return app

@app.route("/get")
async def get_handler(request):
    return text('I am get method')

def test_get_method(app):
    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_headers(app):
    @app.route("/get_with_headers")
    async def get_with_headers(request):
        return text('I am get method', headers={"X-Custom-Header": "value"})

    request, response = app.test_client.get("/get_with_headers")
    assert response.headers.get("X-Custom-Header") == "value"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non_existent_route")
    assert response.status == 404

def test_get_method_empty_response(app):
    @app.route("/empty_response")
    async def empty_response(request):
        return text('')

    request, response = app.test_client.get("/empty_response")
    assert response.text == ''
    assert response.status == 200