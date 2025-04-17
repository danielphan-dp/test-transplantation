import pytest
from sanic import Sanic
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
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.status == 200
    assert response.text == "I am post method"

def test_bp_post_method_not_found(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/invalid_post/")
    assert response.status == 404

def test_bp_post_method_with_data(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post/")
    def post_handler(request):
        return text(f"Received data: {request.json}")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.status == 200
    assert response.text == "Received data: {'key': 'value'}"