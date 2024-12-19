import pytest
from sanic import Sanic
from sanic.response import text, json

@pytest.fixture
def app():
    app = Sanic("TestApp")

    @app.get("/")
    async def handler(request):
        return {}

    return app

def test_get_method_response(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_middleware(app):
    @app.on_response
    def display(_, response):
        response["foo"] = "bar"
        return json(response)

    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get")
    assert response.text == 'I am get method'
    assert response.json["foo"] == "bar"

def test_get_method_not_found(app):
    _, response = app.test_client.get("/nonexistent")
    assert response.status == 404

def test_get_method_empty_request(app):
    @app.get("/get")
    async def get_handler(request):
        return text('I am get method')

    _, response = app.test_client.get("/get", data={})
    assert response.text == 'I am get method'