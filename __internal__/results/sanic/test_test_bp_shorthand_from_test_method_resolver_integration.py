import asyncio
import pytest
from sanic import Sanic, Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    blueprint = Blueprint("test_blueprint")

    @blueprint.post("/post")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(blueprint)
    return app

def test_post_method_success(app):
    request, response = app.test_client.post("/post")
    assert response.body == b"I am post method"

def test_post_method_invalid_method(app):
    request, response = app.test_client.get("/post")
    assert response.status == 405

def test_post_method_with_data(app):
    request, response = app.test_client.post("/post", json={"key": "value"})
    assert response.body == b"I am post method"

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/post", data="")
    assert response.body == b"I am post method"

def test_post_method_with_headers(app):
    headers = {"Custom-Header": "value"}
    request, response = app.test_client.post("/post", headers=headers)
    assert response.body == b"I am post method"