import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    blueprint = Blueprint("test_blueprint")

    @blueprint.put("/put")
    async def put_handler(request):
        return text("I am put method")

    app.blueprint(blueprint)
    return app

def test_put_method(app):
    request, response = app.test_client.put("/put")
    assert response.body == b"I am put method"

def test_put_method_invalid_method(app):
    request, response = app.test_client.get("/put")
    assert response.status == 405

def test_put_method_with_data(app):
    request, response = app.test_client.put("/put", data={"key": "value"})
    assert response.body == b"I am put method"

def test_put_method_empty_body(app):
    request, response = app.test_client.put("/put", data="")
    assert response.body == b"I am put method"

def test_put_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.put("/put", headers=headers)
    assert response.body == b"I am put method"