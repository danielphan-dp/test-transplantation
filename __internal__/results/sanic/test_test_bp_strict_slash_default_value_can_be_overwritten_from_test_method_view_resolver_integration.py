import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    bp = Blueprint("test_text", strict_slashes=True)

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

def test_post_method_with_data(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post_with_data/", strict_slashes=False)
    def post_with_data_handler(request):
        return text(f"Received data: {request.json}")

    app.blueprint(bp)

    request, response = app.test_client.post("/post_with_data/", json={"key": "value"})
    assert response.text == "Received data: {'key': 'value'}"

def test_post_method_with_empty_body(app):
    bp = Blueprint("test_text", strict_slashes=True)

    @bp.post("/post_empty/", strict_slashes=False)
    def post_empty_handler(request):
        return text("Received empty body")

    app.blueprint(bp)

    request, response = app.test_client.post("/post_empty/", data={})
    assert response.text == "Received empty body"