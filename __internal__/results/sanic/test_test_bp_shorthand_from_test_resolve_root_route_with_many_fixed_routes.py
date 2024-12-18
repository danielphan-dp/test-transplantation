import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_get_method(app):
    blueprint = Blueprint("test_get_method")

    @blueprint.get("/get")
    def handler(request):
        return text("I am get method")

    app.blueprint(blueprint)

    request, response = app.test_client.get("/get")
    assert response.body == b"I am get method"

    request, response = app.test_client.post("/get")
    assert response.status == 405

    request, response = app.test_client.put("/get")
    assert response.status == 405

    request, response = app.test_client.delete("/get")
    assert response.status == 405

    request, response = app.test_client.head("/get")
    assert response.status == 405

    request, response = app.test_client.options("/get")
    assert response.status == 405

    request, response = app.test_client.patch("/get")
    assert response.status == 405

    request, response = app.test_client.websocket("/get")
    assert response.status == 405