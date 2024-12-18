import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    blueprint = Blueprint("test_blueprint")

    @blueprint.get("/get")
    def get_handler(request):
        return text("I am get method")

    app.blueprint(blueprint)
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.body == b"I am get method"

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    request, response = app.test_client.get("/get?param=value")
    assert response.body == b"I am get method"

def test_get_method_with_headers(app):
    request, response = app.test_client.get("/get", headers={"Custom-Header": "value"})
    assert response.body == b"I am get method"

def test_get_method_empty_path(app):
    request, response = app.test_client.get("/")
    assert response.status == 404

def test_get_method_with_invalid_route(app):
    request, response = app.test_client.get("/invalid")
    assert response.status == 404