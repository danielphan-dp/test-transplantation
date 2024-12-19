import pytest
from sanic import Sanic
from sanic.blueprints import Blueprint
from sanic.response import text

@pytest.fixture
def app():
    app = Sanic("test_app")
    bp = Blueprint("test_text")

    @bp.get("/get", strict_slashes=True)
    def get_handler(request):
        return text("OK")

    @bp.post("/post/", strict_slashes=True)
    def post_handler(request):
        return text("OK")

    app.blueprint(bp)
    return app

def test_post_method_valid(app):
    request, response = app.test_client.post("/post/")
    assert response.text == "OK"

def test_post_method_invalid_no_slash(app):
    request, response = app.test_client.post("/post")
    assert response.status == 404

def test_post_method_invalid_with_data(app):
    request, response = app.test_client.post("/post/", json={"key": "value"})
    assert response.text == "OK"

def test_post_method_invalid_empty_body(app):
    request, response = app.test_client.post("/post/", data="")
    assert response.text == "OK"

def test_post_method_invalid_method(app):
    request, response = app.test_client.put("/post/")
    assert response.status == 405

def test_post_method_invalid_route(app):
    request, response = app.test_client.post("/nonexistent/")
    assert response.status == 404