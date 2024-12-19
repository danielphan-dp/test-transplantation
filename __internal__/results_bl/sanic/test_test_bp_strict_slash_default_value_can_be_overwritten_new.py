import asyncio
import pytest
from sanic.app import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method_with_strict_slash(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/", strict_slashes=False)
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.text == "OK"

def test_post_method_without_strict_slash(app):
    bp = Blueprint("test_text", strict_slashes=False)

    @bp.post("/post", strict_slashes=False)
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/post")
    assert response.text == "OK"

def test_post_method_with_invalid_route(app):
    bp = Blueprint("test_text", strict_slashes=False)

    @bp.post("/post", strict_slashes=False)
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/invalid_route")
    assert response.status == 404

def test_post_method_with_empty_body(app):
    bp = Blueprint("test_text", strict_slashes=False)

    @bp.post("/post", strict_slashes=False)
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)

    request, response = app.test_client.post("/post", data="")
    assert response.text == "OK"