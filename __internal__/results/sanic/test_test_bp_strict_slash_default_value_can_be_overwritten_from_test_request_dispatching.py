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

def test_post_method_with_different_payload(app):
    bp = Blueprint("test_post_payload", strict_slashes=True)

    @bp.post("/post_with_payload/", strict_slashes=False)
    def post_payload_handler(request):
        return text(request.json.get("key", "No key found"))

    app.blueprint(bp)

    request, response = app.test_client.post("/post_with_payload/", json={"key": "value"})
    assert response.text == "value"

    request, response = app.test_client.post("/post_with_payload/")
    assert response.text == "No key found"