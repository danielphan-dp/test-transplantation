import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("app")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    app = Sanic("app")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404

def test_get_method_with_different_headers():
    app = Sanic("app")

    @app.route("/get", methods=["GET"])
    async def get_method(request):
        return text('I am get method')

    headers = {"Custom-Header": "value"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'