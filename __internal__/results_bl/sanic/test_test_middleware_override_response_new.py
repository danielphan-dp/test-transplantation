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
    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_with_middleware(app):
    @app.middleware("response")
    async def process_response(request, response):
        return text("Middleware Response")

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.text == "Middleware Response"

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_request(app):
    request, response = app.test_client.get("/get", headers={})
    assert response.status == 200
    assert response.text == 'I am get method'