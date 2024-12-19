import logging
import pytest
from sanic import Sanic
from sanic.response import text

def test_get_method_response():
    app = Sanic("test")

    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")
    assert response.status == 200
    assert response.content_type == "text/plain; charset=utf-8"
    assert response.text == 'I am get method'

def test_get_method_invalid_route():
    app = Sanic("test")

    @app.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/invalid")
    assert response.status == 404
    assert response.content_type == "text/plain; charset=utf-8"