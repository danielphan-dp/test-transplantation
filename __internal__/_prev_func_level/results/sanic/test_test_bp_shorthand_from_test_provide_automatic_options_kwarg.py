import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    blueprint = Blueprint("test_post_routes")

    @blueprint.post("/post")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(blueprint)

    request, response = app.test_client.post("/post")
    assert response.body == b"I am post method"

    request, response = app.test_client.get("/post")
    assert response.status == 405

    request, response = app.test_client.put("/post")
    assert response.status == 405

    request, response = app.test_client.delete("/post")
    assert response.status == 405

    request, response = app.test_client.options("/post")
    assert response.status == 405

    request, response = app.test_client.head("/post")
    assert response.status == 405

    request, response = app.test_client.patch("/post")
    assert response.status == 405

    request, response = app.test_client.websocket("/post")
    assert response.status == 405

    request, response = app.test_client.post("/post", data={"key": "value"})
    assert response.body == b"I am post method"  # Testing with additional data

    request, response = app.test_client.post("/post", data="")
    assert response.body == b"I am post method"  # Testing with empty data

    request, response = app.test_client.post("/post", headers={"Content-Type": "application/json"})
    assert response.body == b"I am post method"  # Testing with JSON content type

    request, response = app.test_client.post("/post", headers={"Content-Type": "text/plain"})
    assert response.body == b"I am post method"  # Testing with plain text content type