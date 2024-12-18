import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    blueprint = Blueprint("test_blueprint")

    @blueprint.get("/get")
    def handler(request):
        return text("I am get method")

    app.blueprint(blueprint)
    return app

def test_get_method_success(app):
    request, response = app.test_client.get("/get")
    assert response.body == b"I am get method"

def test_get_method_invalid_method(app):
    request, response = app.test_client.post("/get")
    assert response.status == 405

def test_get_method_with_additional_routes(app):
    @app.get("/another_get")
    def another_handler(request):
        return text("Another GET method")

    request, response = app.test_client.get("/another_get")
    assert response.body == b"Another GET method"

    request, response = app.test_client.post("/another_get")
    assert response.status == 405

def test_get_method_with_query_params(app):
    @app.get("/get_with_params")
    def get_with_params(request):
        param = request.args.get("param", "default")
        return text(f"Param is {param}")

    request, response = app.test_client.get("/get_with_params?param=test")
    assert response.body == b"Param is test"

    request, response = app.test_client.get("/get_with_params")
    assert response.body == b"Param is default"