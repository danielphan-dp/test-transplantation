import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    bp = Blueprint("test_post", strict_slashes=True)

    @bp.post("/post/", strict_slashes=False)
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.text == "I am post method"

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid_post/")
    assert response.status == 404
    assert "Requested URL /invalid_post not found" in response.text

def test_post_method_with_method_not_allowed(app):
    bp = Blueprint("test_post", strict_slashes=True)

    @bp.post("/post/", strict_slashes=False)
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.get("/post/")
    assert response.status == 405
    assert "Method GET not allowed for URL /post/" in response.text

def test_post_method_with_payload(app):
    bp = Blueprint("test_post", strict_slashes=True)

    @bp.post("/post/", strict_slashes=False)
    def post_handler(request):
        return text(f"Received payload: {request.json}")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.text == "Received payload: {'key': 'value'}"