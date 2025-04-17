import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    blueprint = Blueprint("test_blueprint")

    @blueprint.head("/head")
    def head_handler(request):
        return text("OK")

    app.blueprint(blueprint)
    return app

def test_head_method_success(app):
    request, response = app.test_client.head("/head")
    assert response.status == 200
    assert response.body == b""

def test_head_method_not_found(app):
    request, response = app.test_client.head("/nonexistent")
    assert response.status == 404

def test_head_method_with_invalid_method(app):
    request, response = app.test_client.get("/head")
    assert response.status == 405

def test_head_method_empty_response(app):
    request, response = app.test_client.head("/head")
    assert response.body == b""
    assert response.headers['method'] == 'HEAD'