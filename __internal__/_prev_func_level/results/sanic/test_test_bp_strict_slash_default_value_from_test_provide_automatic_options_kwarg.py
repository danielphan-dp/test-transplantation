import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method_with_strict_slash(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_without_strict_slash(app):
    bp = Blueprint("test_text", strict_slashes=False)

    @bp.post("/post")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/post")
    assert response.status == 200
    assert response.text == "I am post method"

def test_post_method_invalid_endpoint(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/invalid_post")
    assert response.status == 404
    assert "Requested URL /invalid_post not found" in response.text

def test_post_method_with_get_request(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.get("/post/")
    assert response.status == 405
    assert "Method GET not allowed for URL /post/" in response.text