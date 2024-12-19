import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == 'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/nonexistent")

    assert response.status == 404

def test_get_method_with_middleware(app):
    blueprint = Blueprint("test_bp_middleware")

    @blueprint.middleware("response")
    async def process_response(request, response):
        return text("OK")

    @app.route("/get")
    async def get_method(request):
        return text('I am get method')

    app.blueprint(blueprint)

    request, response = app.test_client.get("/get")

    assert response.status == 200
    assert response.text == "OK"