import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_bp_post_method(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.status == 200
    assert response.text == "OK"

def test_bp_post_method_no_slash(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/post")
    assert response.status == 404

def test_bp_post_method_invalid_route(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/invalid/")
    assert response.status == 404

def test_bp_post_method_with_payload(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("Received payload")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.status == 200
    assert response.text == "Received payload"