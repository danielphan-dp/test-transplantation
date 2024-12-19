import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

def test_get_method(app: Sanic):
    blueprint = Blueprint("test_get_method")

    @blueprint.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method')

    app.blueprint(blueprint)

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app: Sanic):
    request, response = app.test_client.get("/nonexistent")

    assert response.status == 404

def test_get_method_with_query_params(app: Sanic):
    blueprint = Blueprint("test_get_method_with_query_params")

    @blueprint.route("/get", methods=["GET"])
    def get_method(request):
        return text('I am get method with query params')

    app.blueprint(blueprint)

    request, response = app.test_client.get("/get?param=value")

    assert response.status == 200
    assert response.text == 'I am get method with query params'