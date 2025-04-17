import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_head_method(app):
    blueprint = Blueprint("test_head_routes")

    @blueprint.head("/head")
    def head_handler(request):
        return text('', headers={'method': 'HEAD'})

    app.blueprint(blueprint)

    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.body == b''
    assert response.headers['method'] == 'HEAD'

    request, response = app.test_client.get("/head")
    assert response.status == 405

    request, response = app.test_client.post("/head")
    assert response.status == 405

    request, response = app.test_client.put("/head")
    assert response.status == 405

    request, response = app.test_client.delete("/head")
    assert response.status == 405

    request, response = app.test_client.options("/head")
    assert response.status == 405

    request, response = app.test_client.patch("/head")
    assert response.status == 405