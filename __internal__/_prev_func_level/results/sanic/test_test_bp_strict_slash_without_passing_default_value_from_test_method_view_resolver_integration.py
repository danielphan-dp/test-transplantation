import pytest
from sanic import Sanic
from sanic.response import text
from sanic.blueprints import Blueprint

@pytest.fixture
def app():
    app = Sanic("test_app")
    return app

def test_post_method(app):
    bp = Blueprint("test_post")

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.text == "I am post method"

def test_post_method_with_data(app):
    bp = Blueprint("test_post_data")

    @bp.post("/post/")
    def post_handler(request):
        return text(f"Received data: {request.json}")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.text == "Received data: {'key': 'value'}"

def test_post_method_with_empty_body(app):
    bp = Blueprint("test_post_empty")

    @bp.post("/post/")
    def post_handler(request):
        return text("Received empty body" if not request.body else "Received body")

    app.blueprint(bp)

    request, response = app.test_client.post("/post/")
    assert response.text == "Received empty body"

def test_post_method_not_found(app):
    request, response = app.test_client.post("/nonexistent/")
    assert response.status == 404

def test_post_method_method_not_allowed(app):
    bp = Blueprint("test_post_method_not_allowed")

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    request, response = app.test_client.get("/post/")
    assert response.status == 405
    assert "Method GET not allowed for URL /post/" in response.text