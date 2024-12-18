import asyncio
import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_delete_method(app):
    blueprint = Blueprint("test_delete_routes")

    @blueprint.delete("/delete")
    def delete_handler(request):
        return text("I am delete method")

    app.blueprint(blueprint)

    request, response = app.test_client.delete("/delete")
    assert response.body == b"I am delete method"

    request, response = app.test_client.get("/delete")
    assert response.status == 405

    request, response = app.test_client.put("/delete")
    assert response.status == 405

    request, response = app.test_client.post("/delete")
    assert response.status == 405

    request, response = app.test_client.head("/delete")
    assert response.status == 405

    request, response = app.test_client.options("/delete")
    assert response.status == 405

    request, response = app.test_client.patch("/delete")
    assert response.status == 405

    request, response = app.test_client.websocket("/delete")
    assert response.status == 405