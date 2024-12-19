import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    bp = Blueprint("test_text")

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)
    return app

def test_post_method_success(app):
    request, response = app.test_client.post("/post/")
    assert response.text == "I am post method"

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/invalid/")
    assert response.status == 404

def test_post_method_with_data(app):
    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.text == "I am post method"

def test_post_method_empty_body(app):
    request, response = app.test_client.post("/post/", data="")
    assert response.text == "I am post method"