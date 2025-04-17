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

def test_post_method_with_invalid_route(app):
    request, response = app.test_client.post("/invalid_post/")
    assert response.status == 404
    assert "Requested URL /invalid_post/ not found" in response.text

def test_post_method_with_different_content_type(app):
    bp = Blueprint("test_post")

    @bp.post("/post/")
    def post_handler(request):
        return text("I am post method")

    app.blueprint(bp)

    headers = {"content-type": "application/json"}
    request, response = app.test_client.post("/post/", data='{"key": "value"}', headers=headers)
    assert response.text == "I am post method"