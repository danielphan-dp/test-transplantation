import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method():
    app = Sanic("app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.text == 'I am get method'

def test_get_method_with_invalid_route():
    app = Sanic("app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert "Requested URL /invalid not found" in response.text

def test_get_method_with_custom_header():
    app = Sanic("app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    headers = {"Custom-Header": "Test"}
    request, response = app.test_client.get("/get", headers=headers)
    assert response.text == 'I am get method'
    assert response.status == 200

def test_get_method_with_query_params():
    app = Sanic("app")

    @app.route("/get")
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get?param=value")
    assert response.text == 'I am get method'
    assert response.status == 200