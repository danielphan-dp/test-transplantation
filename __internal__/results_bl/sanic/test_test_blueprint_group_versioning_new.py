import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic(name="test-app")
    return app

@pytest.fixture
def blueprint():
    bp = Blueprint(name="test_bp")
    
    @bp.get("/test-get")
    async def test_get(request):
        return text('I am get method')
    
    return bp

def test_get_method(app, blueprint):
    app.blueprint(blueprint)
    
    request, response = app.test_client.get("/test-get")
    assert response.status == 200
    assert response.body == b'I am get method'

def test_get_method_not_found(app):
    request, response = app.test_client.get("/non-existent-route")
    assert response.status == 404

def test_get_method_invalid_method(app, blueprint):
    app.blueprint(blueprint)
    
    request, response = app.test_client.post("/test-get")
    assert response.status == 405  # Method Not Allowed